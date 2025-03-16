#include <gtk/gtk.h>

static void activate(GtkApplication *app, gpointer user_data) {
    // Create main window
    GtkWidget *window = gtk_application_window_new(app);
    gtk_window_set_title(GTK_WINDOW(window), "NurOS Dark App");
    gtk_window_set_default_size(GTK_WINDOW(window), 800, 600);

    // Create main box with margins
    GtkWidget *main_box = gtk_box_new(GTK_ORIENTATION_VERTICAL, 0);
    gtk_widget_set_margin_start(main_box, 20);
    gtk_widget_set_margin_end(main_box, 20);
    gtk_widget_set_margin_top(main_box, 20);
    gtk_widget_set_margin_bottom(main_box, 20);

    // Create card frame
    GtkWidget *card = gtk_frame_new(NULL);
    gtk_widget_set_halign(card, GTK_ALIGN_CENTER);
    gtk_widget_set_valign(card, GTK_ALIGN_CENTER);
    
    // Create card content box
    GtkWidget *card_box = gtk_box_new(GTK_ORIENTATION_VERTICAL, 10);
    gtk_widget_set_margin_start(card_box, 20);
    gtk_widget_set_margin_end(card_box, 20);
    gtk_widget_set_margin_top(card_box, 20);
    gtk_widget_set_margin_bottom(card_box, 20);

    // Create title label
    GtkWidget *title = gtk_label_new("Welcome to NurOS Dark");
    gtk_widget_add_css_class(title, "title");

    // Create input field
    GtkWidget *input = gtk_entry_new();
    gtk_entry_set_placeholder_text(GTK_ENTRY(input), "Enter something...");
    gtk_widget_set_size_request(input, 400, -1);

    // Create action button
    GtkWidget *button = gtk_button_new_with_label("Perform Action");
    gtk_widget_add_css_class(button, "action-button");

    // Add widgets to card box
    gtk_box_append(GTK_BOX(card_box), title);
    gtk_box_append(GTK_BOX(card_box), input);
    gtk_box_append(GTK_BOX(card_box), button);

    // Add card box to frame
    gtk_frame_set_child(GTK_FRAME(card), card_box);

    // Add card to main box
    gtk_box_append(GTK_BOX(main_box), card);

    // Set window child
    gtk_window_set_child(GTK_WINDOW(window), main_box);

    // Load CSS
    GtkCssProvider *provider = gtk_css_provider_new();
    const char *css_data = 
        "window {"
        "   background-color: #1a1a1a;"
        "}"
        "frame {"
        "   background-color: #2d2d2d;"
        "   border-radius: 10px;"
        "   margin: 10px;"
        "}"
        ".title {"
        "   color: white;"
        "   font-size: 24px;"
        "   font-weight: bold;"
        "   margin-bottom: 20px;"
        "}"
        "entry {"
        "   background-color: #3d3d3d;"
        "   color: white;"
        "   border: none;"
        "   border-radius: 5px;"
        "   padding: 10px;"
        "   margin: 10px 0;"
        "}"
        "entry:focus {"
        "   background-color: #454545;"
        "   border: 2px solid #5c90ff;"
        "}"
        ".action-button {"
        "   background-color: #5c90ff;"
        "   color: white;"
        "   border: none;"
        "   border-radius: 5px;"
        "   padding: 12px;"
        "   margin-top: 10px;"
        "   font-weight: bold;"
        "}"
        ".action-button:hover {"
        "   background-color: #4a7ae0;"
        "}"
        ".action-button:active {"
        "   background-color: #3e68c7;"
        "}";

    gtk_css_provider_load_from_string(provider, css_data);

    gtk_style_context_add_provider_for_display(
        gdk_display_get_default(),
        GTK_STYLE_PROVIDER(provider),
        GTK_STYLE_PROVIDER_PRIORITY_APPLICATION
    );

    // Show window using the new method
    gtk_window_present(GTK_WINDOW(window));
}

int main(int argc, char **argv) {
    GtkApplication *app = gtk_application_new("com.example.nurOS.dark",
                                            G_APPLICATION_DEFAULT_FLAGS);
    g_signal_connect(app, "activate", G_CALLBACK(activate), NULL);
    int status = g_application_run(G_APPLICATION(app), argc, argv);
    g_object_unref(app);

    return status;
}