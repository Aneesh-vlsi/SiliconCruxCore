# SiliconCrux Core v3.0

An intelligent, high-fidelity Electronic Design Automation (EDA) Physical Design Assistant designed for early-stage chip floorplanning and real-time interconnect length optimization.

---

## 🛠️ The Problem Statement

In modern VLSI (Very Large Scale Integration) systems, Design Verification (DV) and Physical Design (RTL-to-GDSII) cycles consume up to **70% of total product development schedules**. Traditional commercial simulation suites are heavy, multi-gigabyte platforms that require substantial compilation times to evaluate trivial macro block layout adjustments.

Architects and physical design engineers lack a lightweight, instantaneous prototyping platform to experiment with macro placement strategies, identify routing congestion bottlenecks, and optimize signal wire lengths before initializing computationally intensive, hours-long EDA tool operations.

---

## 🚀 The Solution: SiliconCrux Core

**SiliconCrux Core** acts as an interactive, real-time physical prototyping scratchpad. By combining high-performance analytical modeling with a multi-pane hardware database cockpit, it allows chip layout designers to map spatial configurations and receive instant geometric telemetry feedback in **milliseconds** rather than hours.

### Key Capabilities:
*   **Analytical Interconnect Modeling (HPWL Engine):** Computes layout wire distance trends using the industry-standard **Half-Perimeter Wirelength (HPWL)** formulation.
*   **Dynamic Ratsnest Layout Tracking:** Live-renders signal flightlines across relational pin connection nets, automatically shifting interconnect pathways during drag-and-drop operations.
*   **Automated Design Object Classification:** Leverages a custom structural parser to automatically categorize custom-deployed macros (Logic, Memory, Analog) into a clean hierarchy database tree.
*   **Production CAD Rendering Pipeline:** Built using a touch-optimized UI framework, enabling smooth visual tracking and precise boundary alignment loupe features.
