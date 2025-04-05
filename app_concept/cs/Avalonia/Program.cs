using Avalonia;
using Avalonia.Controls;
using Avalonia.Controls.ApplicationLifetimes;
using Avalonia.Input;
using Avalonia.Interactivity;
using Avalonia.Layout;
using Avalonia.Media;
using Avalonia.Styling;
using Avalonia.Themes.Fluent;
using System;
using System.Runtime.InteropServices;

namespace NurOSDark
{
    public class App : Application
    {
        public override void Initialize()
        {
            Styles.Add(new FluentTheme());
        }

        public override void OnFrameworkInitializationCompleted()
        {
            if (ApplicationLifetime is IClassicDesktopStyleApplicationLifetime desktop)
            {
                desktop.MainWindow = new MainWindow();
            }
            base.OnFrameworkInitializationCompleted();
        }
    }

    public class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
        }

        private void InitializeComponent()
        {
            Title = "NurOS Dark App";
            Width = 800;
            Height = 600;

            // Создаем карточку
            var card = new Border
            {
                Background = new SolidColorBrush(Color.Parse("#2d2d2d")),
                CornerRadius = new CornerRadius(10),
                Padding = new Thickness(20),
                Width = 400,
                HorizontalAlignment = HorizontalAlignment.Center,
                VerticalAlignment = VerticalAlignment.Center
            };

            var stackPanel = new StackPanel();

            // Заголовок
            var title = new TextBlock
            {
                Text = "Welcome to NurOS Dark",
                Foreground = Brushes.White,
                FontSize = 24,
                FontWeight = FontWeight.Bold,
                Margin = new Thickness(0, 0, 0, 20)
            };

            // Поле ввода
            var input = new TextBox
            {
                Watermark = "Enter something...",
                Background = new SolidColorBrush(Color.Parse("#3d3d3d")),
                Foreground = Brushes.White,
                CornerRadius = new CornerRadius(5),
                Padding = new Thickness(10),
                FontSize = 14,
                Margin = new Thickness(0, 10)
            };

            // Кнопка действия
            var button = new Button
            {
                Content = "Perform Action",
                Background = new SolidColorBrush(Color.Parse("#5c90ff")),
                Foreground = Brushes.White,
                CornerRadius = new CornerRadius(5),
                Padding = new Thickness(12),
                FontSize = 14,
                FontWeight = FontWeight.Bold,
                Margin = new Thickness(0, 10, 0, 0),
                HorizontalAlignment = HorizontalAlignment.Stretch
            };

            // События для интерактивности кнопки
            button.PointerPressed += (s, e) => 
                button.Background = new SolidColorBrush(Color.Parse("#3e68c7"));
            
            button.PointerReleased += (s, e) => 
                button.Background = new SolidColorBrush(Color.Parse("#5c90ff"));

            // Добавляем все элементы в стек-панель
            stackPanel.Children.Add(title);
            stackPanel.Children.Add(input);
            stackPanel.Children.Add(button);

            // Добавляем стек-панель в карточку
            card.Child = stackPanel;

            // Устанавливаем карточку как содержимое окна
            Content = card;
        }
    }

    public class Program
    {
        [STAThread]
        public static void Main(string[] args)
        {
            if (!RuntimeInformation.IsOSPlatform(OSPlatform.Linux))
            {
                Console.WriteLine("This application is designed to run only on Linux!");
                Environment.Exit(1);
                return;
            }

            try
            {
                BuildAvaloniaApp()
                    .StartWithClassicDesktopLifetime(args);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Application crashed: {ex.Message}");
                Environment.Exit(1);
            }
        }

        public static AppBuilder BuildAvaloniaApp()
            => AppBuilder.Configure<App>()
                .UsePlatformDetect()
                .With(new X11PlatformOptions())
                .LogToTrace();
    }
}