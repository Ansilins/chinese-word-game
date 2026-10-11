// The speech checker: a Whisper model that runs on this device, in a worker so the game stays responsive.
// The page sends {type:"load"} once, then {type:"run", id, audio} with 16 kHz mono audio for each word.
let asr = null;

async function load() {
  const T = await import("./vendor/transformers.min.js");
  T.env.allowLocalModels = false;
  // the model is kept in this game's own cache ("cwg-" like every other key), not the shared default one
  T.env.useBrowserCache = false;
  T.env.useCustomCache = true;
  T.env.customCache = await caches.open("cwg-model");
  T.env.backends.onnx.wasm.wasmPaths = new URL("./vendor/", self.location.href).href;
  T.env.backends.onnx.wasm.numThreads = 1;
  const files = {};
  asr = await T.pipeline("automatic-speech-recognition", "Xenova/whisper-base", {
    dtype: "q8", device: "wasm",
    progress_callback: p => {
      if (p.status !== "progress" || !p.total) return;
      files[p.file] = [p.loaded, p.total];
      const v = Object.values(files), got = v.reduce((a, x) => a + x[0], 0), all = v.reduce((a, x) => a + x[1], 0);
      postMessage({ type: "progress", pct: Math.floor(got / all * 100) });
    },
  });
}

self.onmessage = async e => {
  const m = e.data;
  if (m.type === "load") {
    try { await load(); postMessage({ type: "ready" }); }
    catch (err) { postMessage({ type: "error", message: String(err && err.message || err) }); }
  } else if (m.type === "run") {
    try {
      const r = await asr(m.audio, { language: "chinese", task: "transcribe" });
      postMessage({ type: "result", id: m.id, text: (r.text || "").trim() });
    } catch (err) { postMessage({ type: "error", id: m.id, message: String(err && err.message || err) }); }
  }
};
