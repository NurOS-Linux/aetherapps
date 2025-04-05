using Gtk;
using System;

class Program
{
    static void Main()
    {
        Application.Init();

        var win = new Window("NurOS Dark App")
        {
            DefaultWidth = 800,
            DefaultHeight = 600,
            WindowPosition = WindowPosition.Center
        };

        // Create main container
        var mainBox = new Box(Orientation.Vertical, 0);
        win.Add(mainBox);

        // Create centered card container
        var alignment = new Box(Orientation.Vertical, 0);
        alignment.Expand = true;
        alignment.Valign = Align.Center;
        alignment.Halign = Align.Center;
        mainBox.Add(alignment);

        // Create card frame
        var card = new Frame();
        card.Name = "card";
        alignment.Add(card);

        // Create card content
        var cardBox = new Box(Orientation.Vertical, 10);
        cardBox.MarginStart = 20;
        cardBox.MarginEnd = 20;
        cardBox.MarginTop = 20;
        cardBox.MarginBottom = 20;
        card.Add(cardBox);

        // Title label
        var title = new Label("Welcome to NurOS Dark");
        title.Name = "title";
        cardBox.Add(title);

        // Input field
        var inputField = new Entry();
        inputField.Name = "input";
        inputField.PlaceholderText = "Enter something...";
        cardBox.Add(inputField);

        // Action button
        var actionButton = new Button("Perform Action");
        actionButton.Name = "actionButton";
        cardBox.Add(actionButton);

        // Apply CSS styling
        var cssProvider = new CssProvider();
        cssProvider.LoadFromData(@"
            window {
                background: #1a1a1a;
            }

            frame#card {
                background: #2d2d2d;
                border-radius: 10px;
                border: none;
                min-height: 200px;
                min-width: 400px;
            }

            label#title {
                color: #ffffff;
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 20px;
            }

            entry#input {
                background: #3d3d3d;
                border: none;
                border-radius: 5px;
                padding: 10px;
                color: #ffffff;
                font-size: 14px;
                margin: 10px 0;
            }

            entry#input:focus {
                background: #454545;
                border: 2px solid #5c90ff;
            }

            button#actionButton {
                background: #5c90ff;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 12px;
                font-size: 14px;
                font-weight: bold;
                margin-top: 10px;
            }

            button#actionButton:hover {
                background: #4a7ae0;
            }

            button#actionButton:active {
                background: #3e68c7;
            }
        ");

        // Apply CSS to the window and all its children
        win.StyleContext.AddProvider(cssProvider, uint.MaxValue);
        mainBox.StyleContext.AddProvider(cssProvider, uint.MaxValue);
        card.StyleContext.AddProvider(cssProvider, uint.MaxValue);
        title.StyleContext.AddProvider(cssProvider, uint.MaxValue);
        inputField.StyleContext.AddProvider(cssProvider, uint.MaxValue);
        actionButton.StyleContext.AddProvider(cssProvider, uint.MaxValue);

        // Connect destroy event
        win.DeleteEvent += (o, args) => Application.Quit();

        win.ShowAll();
        Application.Run();
    }
}