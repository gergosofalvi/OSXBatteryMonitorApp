
# BatteryMonitorApp

![](https://raw.githubusercontent.com/gergosofalvi/OSXBatteryMonitorApp/main/battery_monitor.gif)

A simple and visually appealing battery monitoring application built with PyQt5. It displays real-time battery wattage usage and includes features such as dark/light mode switching with emoji buttons and a dynamic progress bar for visualizing the current charge state.

## Features

- Displays real-time battery wattage usage.
- Automatically starts in dark mode.
- Switch between dark and light modes using an emoji button.
- Color-coded progress bar:
  - **Green**: Above 60W.
  - **Yellow**: Between 20W and 60W.
  - **Red**: Below 20W.
- Minimalistic and easy-to-use interface.

## Installation

1. Clone the repository:
   ```bash
   git clone [https://github.com/gergosofalvi/OSXBatteryMonitorApp.git](https://github.com/gergosofalvi/OSXBatteryMonitorApp.git)
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python battery_monitor.py
   ```
   Or Download release : [https://github.com/gergosofalvi/OSXBatteryMonitorApp/releases/](https://github.com/gergosofalvi/OSXBatteryMonitorApp/releases/)

## Packaging the Application

To create a standalone executable, you can use PyInstaller:

```bash
pyinstaller --onefile --windowed --icon=battery_monitor.icns battery_monitor.py
```

This will generate a `.app` or `.exe` file in the `dist` folder.

## License

This project is licensed under the MIT License.
