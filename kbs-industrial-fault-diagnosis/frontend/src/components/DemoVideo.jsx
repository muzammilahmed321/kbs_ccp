import { PlayCircle } from "lucide-react";
import { siteConfig } from "../config/siteConfig.js";

function toYouTubeEmbed(url) {
  try {
    const u = new URL(url);
    if (u.hostname.includes("youtu.be")) return `https://www.youtube.com/embed/${u.pathname.slice(1)}`;
    if (u.hostname.includes("youtube.com")) {
      if (u.pathname.startsWith("/embed/")) return url;
      const id = u.searchParams.get("v");
      if (id) return `https://www.youtube.com/embed/${id}`;
    }
  } catch { /* local video path */ }
  return null;
}

function VideoPlayer({ src, poster, title }) {
  const embed = toYouTubeEmbed(src);
  return embed ? (
    <iframe src={embed} title={title} allow="accelerometer; autoplay; clipboard-write; encrypted-media; picture-in-picture" allowFullScreen />
  ) : (
    <video controls preload="metadata" poster={poster || undefined}><source src={src} />Your browser does not support the video tag.</video>
  );
}

export default function DemoVideo() {
  const { demoVideo } = siteConfig;
  return (
    <section id="demo" className="section demo-section">
      <div className="container demo-container">
        <div className="demo-heading"><p className="eyebrow">Project walkthrough</p><h2>See FaultSense AI <span className="accent">in action.</span></h2></div>
        <div className="video-frame">
          {demoVideo.src ? <VideoPlayer {...demoVideo} /> : <div className="video-placeholder"><PlayCircle size={58} strokeWidth={1.4} /><strong>Demo video</strong></div>}
        </div>
      </div>
    </section>
  );
}
