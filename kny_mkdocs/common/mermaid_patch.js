let mermaidRef;
Object.defineProperty(window, "mermaid", {
  configurable: true,
  get: () => mermaidRef,
  set(m) {
    mermaidRef = m;
    const init = m.initialize.bind(m);
    m.initialize = (cfg = {}) =>
      init({
        ...cfg,
        themeCSS: (cfg.themeCSS || "") + `
          .treeView-node-label { fill: var(--md-default-fg-color) !important; }
          .treeView-node-line  { stroke: var(--md-default-fg-color) !important; }
        `
      });
  }
});
