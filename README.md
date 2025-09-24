# Conway Traffic Simulation

An innovative traffic simulation system that uses cellular automata (Conway's Game of Life rules) to model traffic flow patterns. Watch as traffic evolves organically based on simple rules, creating realistic traffic behaviors and congestion patterns.

## 🚗 What is Conway Traffic?

Conway Traffic simulates traffic flow using three types of road elements:

- **🟠 Orange Barriers**: Static obstacles (traffic lights, construction zones, roadblocks)
- **🔵 Moving Traffic**: Vehicles that follow traffic rules and evolve based on their surroundings  
- **⚫ Empty Roads**: Available space for traffic to flow

## 🌟 Key Features

- **Interactive Traffic Design**: Click to place barriers and traffic
- **Real-time Simulation**: Watch traffic patterns evolve automatically
- **Smart Traffic Rules**: Vehicles move according to realistic traffic behavior
- **Save & Load Patterns**: Store your traffic scenarios for later use
- **Customizable Grid**: Resize your traffic network as needed

## 🎯 Use Cases

- **Urban Planning**: Test traffic flow in proposed road designs
- **Education**: Learn about cellular automata and traffic modeling
- **Research**: Study emergent traffic behaviors and congestion patterns
- **Entertainment**: Create and watch fascinating traffic animations

## 🚀 Quick Start

1. **Run the App**: `python nicegui_app/app.py`
2. **Design Your Roads**: Click cells to place barriers (orange) and traffic (blue)
3. **Start Simulation**: Hit "Run" to watch traffic evolve
4. **Experiment**: Try different patterns and see what happens!

## 🔬 The Science Behind It

This simulation is based on Conway's Game of Life, a cellular automaton where simple rules create complex, emergent behaviors. In our traffic adaptation:

- Traffic vehicles (blue) follow Conway's rules: they survive if they have 2-3 neighbors, and new traffic appears if empty spaces have exactly 3 traffic neighbors
- Barriers (orange) remain static, creating traffic constraints
- The result is realistic traffic flow patterns that emerge from simple local interactions

## 📊 What You'll Discover

- How small changes in road layout affect traffic flow
- Natural traffic congestion and bottleneck formation
- Self-organizing traffic patterns
- The beauty of emergent behavior in complex systems

Perfect for students, researchers, urban planners, or anyone fascinated by how simple rules can create complex, lifelike behaviors!
