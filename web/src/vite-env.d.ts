/// <reference types="vite/client" />

// jsdom does not implement SVG layout; setup.ts stubs getBBox so d3 code can run.
interface SVGElement {
  getBBox(): DOMRect
}
