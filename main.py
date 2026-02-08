import gi
import asyncio
import threading
import requests
import cv2
import numpy as np
import io
import queue
from PIL import Image
from ultralytics import YOLO
import websockets

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, GLib, Gio, Gdk, GdkPixbuf

class RobotControlApp(Adw.Application):
    def __init__(self):
        super().__init__(application_id='com.nucleus.robot.yolo', 
                         flags=Gio.ApplicationFlags.FLAGS_NONE)
        
        # YOLO & Logic
        self.model = YOLO("yolov8n.pt")
        self.conf_threshold = 0.3
        self.image_queue = queue.Queue(maxsize=1)
        self.is_tracking = False
        self.ws_uri = "ws://192.168.4.1:1606"
        self.image_url = "http://192.168.4.1:1607/capture"
        self.ws = None
        self.loop = asyncio.new_event_loop()

    def do_activate(self):
        # Glavni prozor
        self.win = Adw.ApplicationWindow(application=self)
        self.win.set_title("YOLOv8 Robot Control Pro")
        self.win.set_default_size(1000, 800)

        # Glavni kontejner
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.win.set_content(vbox)

        # Header Bar
        header = Adw.HeaderBar()
        vbox.append(header)

        # Horizontalni split (Video | Logovi/Kontrole)
        content_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        vbox.append(content_box)

        # --- LEVA STRANA: Video Feed ---
        video_stack = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        video_stack.set_margin_all(20)
        video_stack.set_hexpand(True)

        self.video_image = Gtk.Image()
        self.video_image.set_vexpand(True)
        self.video_image.set_valign(Gtk.Align.CENTER)
        video_stack.append(self.video_image)

        # Kontrole ispod videa
        ctrl_card = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        ctrl_card.set_halign(Gtk.Align.CENTER)
        
        self.track_btn = Gtk.Button(label="🍌 Pokreni praćenje")
        self.track_btn.add_css_class("suggested-action")
        self.track_btn.connect("clicked", self.toggle_tracking)
        ctrl_card.append(self.track_btn)

        video_stack.append(ctrl_card)
        content_box.append(video_stack)

        # --- DESNA STRANA: Status ---
        status_panel = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        status_panel.set_size_request(250, -1)
        status_panel.add_css_class("sidebar")
        status_panel.set_margin_all(10)

        status_panel.append(Gtk.Label(label="ROBOT TELEMETRY", xalign=0))
        
        self.status_label = Gtk.Label(label="Status: Disconnected")
        status_panel.append(self.status_label)

        content_box.append(status_panel)

        # Keyboard Bindings
        evk = Gtk.EventControllerKey()
        evk.connect("key-pressed", self.on_key_down)
        evk.connect("key-released", self.on_key_up)
        self.win.add_controller(evk)

        # CSS
        self.load_css()

        # Start Threads
        threading.Thread(target=self.run_asyncio_loop, daemon=True).start()
        threading.Thread(target=self.video_stream_thread, daemon=True).start()
        
        # UI Refresh Timer (GLib)
        GLib.timeout_add(30, self.update_ui_image)

        self.win.present()

    def load_css(self):
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path("style.css")
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def add_log(self, msg):
        print(f"Log: {msg}") # Može se dodati u Gtk.ListBox po želji

    def toggle_tracking(self, btn):
        self.is_tracking = not self.is_tracking
        if self.is_tracking:
            btn.set_label("🛑 Zaustavi praćenje")
            btn.add_css_class("destructive-action")
        else:
            btn.set_label("🍌 Pokreni praćenje")
            btn.remove_css_class("destructive-action")
            self.send_command('stop')

    def video_stream_thread(self):
        while True:
            try:
                response = requests.get(self.image_url, timeout=2)
                if response.status_code == 200:
                    img_array = np.frombuffer(response.content, dtype=np.uint8)
                    frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

                    # YOLO Detekcija
                    results = self.model.predict(frame, conf=self.conf_threshold, verbose=False)
                    annotated_frame = results[0].plot()

                    # Tracking logika (Banana = 46)
                    if self.is_tracking:
                        self.process_tracking(results[0], frame.shape[1])

                    # Priprema za GTK
                    _, buffer = cv2.imencode('.png', annotated_frame)
                    GLib.idle_add(self.update_image_data, buffer.tobytes())
            except Exception as e:
                print(f"Stream error: {e}")

    def update_image_data(self, data):
        loader = GdkPixbuf.PixbufLoader.new_with_type("png")
        loader.write(data)
        loader.close()
        pixbuf = loader.get_pixbuf()
        self.video_image.set_from_pixbuf(pixbuf)
        return False

    def update_ui_image(self):
        return True # Nastavlja tajmer

    def process_tracking(self, result, width):
        found = False
        for box in result.boxes:
            if int(box.cls.item()) == 46:
                found = True
                x1, _, x2, _ = box.xyxy[0].tolist()
                cx = (x1 + x2) / 2
                offset = cx - (width / 2)
                
                if abs(offset) < 80: self.send_command('napred')
                elif offset < 0: self.send_command('levo')
                else: self.send_command('desno')
                break
        if not found: self.send_command('stop')

    def on_key_down(self, ctrl, keyval, keycode, state):
        if self.is_tracking: return True
        key = Gdk.keyval_name(keyval)
        mapping = {"Up": "napred", "Down": "nazad", "Left": "levo", "Right": "desno", "space": "stop"}
        if key in mapping:
            self.send_command(mapping[key])
        return True

    def on_key_up(self, ctrl, keyval, keycode, state):
        if not self.is_tracking:
            self.send_command("stop")
        return True

    def send_command(self, cmd):
        asyncio.run_coroutine_threadsafe(self.async_send(cmd), self.loop)

    async def async_send(self, cmd):
        if self.ws and not self.ws.closed:
            try: await self.ws.send(cmd)
            except: pass

    def run_asyncio_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.websocket_manager())

    async def websocket_manager(self):
        while True:
            try:
                async with websockets.connect(self.ws_uri) as websocket:
                    self.ws = websocket
                    GLib.idle_add(self.status_label.set_text, "Status: CONNECTED")
                    while not websocket.closed:
                        await asyncio.sleep(0.1)
            except:
                GLib.idle_add(self.status_label.set_text, "Status: RECONNECTING...")
                await asyncio.sleep(2)

if __name__ == "__main__":
    app = RobotControlApp()
    app.run()