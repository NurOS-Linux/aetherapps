#include <Elementary.h>
#include <time.h>
#include <stdio.h>

typedef struct {
    Evas_Object *win;
    Evas_Object *label_time;
    Evas_Object *label_user;
} App_Data;

static char *get_utc_time(void) {
    time_t now = time(NULL);
    struct tm *tm_utc = gmtime(&now);
    static char buf[64];
    strftime(buf, sizeof(buf), "%Y-%m-%d %H:%M:%S", tm_utc);
    return buf;
}

static void win_delete_cb(void *data, Evas_Object *obj, void *event_info) {
    elm_exit();
}

static Eina_Bool update_clock(void *data) {
    App_Data *ad = data;
    char buf[128];
    snprintf(buf, sizeof(buf), "Current Date and Time (UTC - YYYY-MM-DD HH:MM:SS formatted):<br>%s", get_utc_time());
    elm_object_text_set(ad->label_time, buf);
    return EINA_TRUE;
}

EAPI_MAIN int elm_main(int argc, char **argv) {
    App_Data ad = {0};
    
    // Создаем главное окно
    ad.win = elm_win_util_standard_add("clock", "System Info");
    elm_win_autodel_set(ad.win, EINA_TRUE);
    evas_object_smart_callback_add(ad.win, "delete,request", win_delete_cb, NULL);
    
    // Основной контейнер
    Evas_Object *box = elm_box_add(ad.win);
    evas_object_size_hint_weight_set(box, EVAS_HINT_EXPAND, EVAS_HINT_EXPAND);
    elm_win_resize_object_add(ad.win, box);
    evas_object_show(box);
    
    // Метка для времени
    ad.label_time = elm_label_add(ad.win);
    elm_label_line_wrap_set(ad.label_time, ELM_WRAP_WORD);
    evas_object_size_hint_weight_set(ad.label_time, EVAS_HINT_EXPAND, 0.0);
    evas_object_size_hint_align_set(ad.label_time, EVAS_HINT_FILL, 0.5);
    elm_box_pack_end(box, ad.label_time);
    evas_object_show(ad.label_time);
    
    // Разделитель
    Evas_Object *separator = elm_separator_add(ad.win);
    elm_separator_horizontal_set(separator, EINA_TRUE);
    elm_box_pack_end(box, separator);
    evas_object_show(separator);
    
    // Метка для имени пользователя
    ad.label_user = elm_label_add(ad.win);
    char user_text[128];
    snprintf(user_text, sizeof(user_text), "Current User's Login:<br>Хз"); 
    elm_object_text_set(ad.label_user, user_text);
    evas_object_size_hint_weight_set(ad.label_user, EVAS_HINT_EXPAND, 0.0);
    evas_object_size_hint_align_set(ad.label_user, EVAS_HINT_FILL, 0.5);
    elm_box_pack_end(box, ad.label_user);
    evas_object_show(ad.label_user);
    
    // Устанавливаем размер окна и показываем его
    evas_object_resize(ad.win, 400, 200);
    evas_object_show(ad.win);
    
    // Создаем таймер для обновления времени
    ecore_timer_add(1.0, update_clock, &ad);
    update_clock(&ad); // Начальное обновление
    
    elm_run();
    elm_shutdown();
    
    return 0;
}
ELM_MAIN()