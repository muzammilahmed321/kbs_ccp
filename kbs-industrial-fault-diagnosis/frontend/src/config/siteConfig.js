// ---------------------------------------------------------------
// EDIT THIS FILE to change text, links, stats, team and the video.
// ---------------------------------------------------------------
export const siteConfig = {
  brand: "FaultSense AI",
  tagline: "Explainable Diagnosis. Smarter Maintenance.",
  course: "Knowledge Based System (CT-359)",
  department: "Department of Computer Science & Information Technology",

  // Hero background. Replace with your own photo if you like.
  heroImage: "/images/milling-machine.webp",

  // "Try It Live" buttons open this address.
  // Local FastAPI backend: http://127.0.0.1:8000/docs
  liveDemoUrl: "http://127.0.0.1:8000/docs",

  // Set to false to hide the statistics strip under the hero.
  showStats: false,
  // Every number below was measured on the AI4I 2020 dataset in this project.
  stats: [
    { icon: "layers", value: "5", label: "Fault modes", note: "TWF · HDF · PWF · OSF · RNF" },
    { icon: "database", value: "10,000", label: "Machine records", note: "AI4I 2020 dataset" },
    { icon: "shield", value: "100%", label: "Rule precision", note: "HDF · PWF · OSF on the dataset" },
    { icon: "search", value: "Explainable", label: "Every diagnosis", note: "shows exactly why" },
  ],

  // DEMO VIDEO
  //  - Local file:  src: "/videos/demo.mp4"   (put the file in public/videos/)
  //  - YouTube:     src: "https://www.youtube.com/watch?v=XXXXXXXXXXX"
  //  - Leave "" to show the "coming soon" placeholder.
  demoVideo: {
    src: "",
    poster: "",
    title: "FaultSense AI live demo",
  },

  team: [
    { name: "Izma Warsia", role: "(CT- 24311)", photo: "" },
    { name: "Safa Khurram", role: "(CT-24310)", photo: "" },
    { name: "Muzammil Ahmed", role: "(CT-24307)", photo: "" },
    { name: "Daniyal Hussain", role: "(CT-24093)", photo: "" },
    { name: "Habib-ul-Rehman", role: "(CT-24080)", photo: "" },
  ],

  // Replace these placeholders with your real details.
  contact: {
    email: "your-email@example.com",
    github: "https://github.com/your-username/your-repo",
    linkedin: "https://www.linkedin.com/",
  },
};
