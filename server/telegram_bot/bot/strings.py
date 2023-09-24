welcome_message = "Привет, я бот для регистраций на экпертизы"

# Menu
main_menu_message = "Что бы вы хотели сделать?"
select_date_message = "Выберите пожалуйста подходящую дату"
select_hour_message = "Выберите пожалуйста время проведения экспертизы"

# Message
registration_complete = "Регистрация завершена, можно пользоваться ботом!"
examination_register_wait_examinator = "Происходит подбор специалиста..."
examination_register_complete = "Вы успешно зарегистрировались на экспертизу!"

my_examinations_message = "Мои экспертизы:"
my_examination_btn_data = "📅 {0} | ⌚ {1:02}:00"
my_examination_full = "🧑 Имя: {0}\n📅 Дата: {1}\n⌚ Время: {2:02}:00 - {3:02}:00\n🏡 Дом/Квартира: {4}\n{5}"
client_contact = "📱 Telegram для связи: @{0}"

operator_help_contact = "Контакты оператора:\n@inex550"

examination_register_complete_for_expert = "К вам зарегистрировались на экспертизу!\n\n📅 Дата: {0}\n⌚ Время: {1:02}:00 - {2:02}:00\n📱 Telegram для связи: {3}"

registration_canceled = "Регистрация отменена"

not_implemented = "Кнопка не доступна"

admin_success = "Теперь вы сотрудник"
admin_failed = "\\(>_<)/"

# Inputs
input_full_name = "Введите ваше имя"
input_location = "Пришлите пожалуйста геолокацию места для проведения экспертизы"
input_house = "Пришлите пожалуйста номер дома / квартиры или иные уточняющие данные"

# Errors
error_unknown = "Произошла неизвестная ошибка. Попробуйте ещё раз позже"

error_full_name = "Имя указано неверно. Проверьте пожалуйста, что имя не слишком короткое и не содержит цифр"
error_no_location = "Локация была указана неверно. Вам нужно прикрепить геолокацию, нажав на скрепку справа от ввода и выбрав нужную локацию в соответствующем пункте"
error_examination_register = "Произошла ошибка при создании экспертизы. Попробуйте позже"
error_no_such_expert = "Мы не смогли найти подходящего эксперта. Возможно они все заняты. Попробуйте зарегистрироваться на другое время"

error_no_one_examination = "В данный момент вы не зарегистрированы ни на одну экспертизу"
error_no_one_metric = "В данный момент в системе отсутствуют экспертизы"

error_date = "Можно выбрать дату только начиная с текущего дня"

# Buttons
btn_cancel_examination = "Отменить запись"
btn_register_examination = "Записаться на экспертизу"
btn_move_examination = "Перенести экпертизу"
btn_my_examinations = "Мои экпертизы"
btn_operator_help = "Помощь оператора"

btn_expert_statistics = "Скачать метрики"

btn_back = "Назад"
btn_cancel = "Отмена"

# Callbacks
cb_cancel_examination = "cb_cancel_examination"
cb_register_examination = "cb_register_examination"
cb_move_examination = "cb_move_examination"
cb_client_examinations = "cb_client_examinations"
cb_expert_examinations = "cb_expert_examinations"
cb_operator_help = "cb_operator_help"

cb_expert_statistics = "cb_expert_statistics"

cb_pick_examination_date = "cb_pick_examination_date"
cb_pick_examination_hour = "cb_pick_examination_hour"

cb_back = "cb_back"
cb_cancel = "cb_cancel"

cb_cancel_examination_creation = "cb_cancel_examination_creation"