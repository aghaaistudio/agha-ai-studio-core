document.addEventListener("DOMContentLoaded", () => {
  const cards = document.querySelectorAll("section, article, a, button");

  cards.forEach(card => {
    const text = card.innerText?.trim() || "";
    if (!["AI Models", "API Platform", "Usage & Credits"].includes(text)) return;

    card.style.cursor = "pointer";
    card.addEventListener("click", () => {
      const name = text;
      const panel = document.createElement("div");
      panel.style.cssText = "position:fixed;inset:0;z-index:9999;background:#180914ee;display:grid;place-items:center;padding:20px;";
      const box = document.createElement("div");
      box.style.cssText = "max-width:420px;width:100%;padding:24px;border:1px solid #c75a8c;border-radius:20px;background:#3b172d;color:white;font-family:Arial,sans-serif;";
      const heading = document.createElement("h2");
      heading.textContent = name;
      const message = document.createElement("p");
      message.textContent = name === "AI Models"
        ? "AI provider connections will be configured securely on the server."
        : name === "API Platform"
        ? "API application management is the next backend module to implement."
        : "Real usage and credits require backend metering.";
      const close = document.createElement("button");
      close.textContent = "Close";
      close.style.cssText = "padding:10px 18px;border:0;border-radius:10px;background:#c43d78;color:white;";
      close.addEventListener("click", () => panel.remove());
      box.append(heading, message, close);
      panel.append(box);
      document.body.append(panel);
    });
  });
});
