import { Cog } from "lucide-react";
import { siteConfig } from "../config/siteConfig.js";

export default function Logo() {
  const [first, ...rest] = siteConfig.brand.split(" ");
  return (
    <a href="#home" className="logo" aria-label={siteConfig.brand}>
      <Cog size={34} strokeWidth={1.8} />
      <span>
        {first} <em>{rest.join(" ")}</em>
      </span>
    </a>
  );
}
