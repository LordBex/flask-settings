
import * as ElementParser from './utils/element_parser.js'
import {config} from './init.js'

function get_setting_form_data(setting_form){
    let data = {};
    $(setting_form)
        .find(".settings-element")
        .each(function () {
            let [element_key, element_value] = ElementParser.parse_element(this)
            data[element_key] = element_value
        });
    return data
}

window.flasky_settings.send_form_data = function(url, data){
            // sending requeset
            fetch(url, {
                method: "post",
                headers: {
                    Accept: "application/json",
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(data),
            })
                .then(function (response) {     // SUCCESS
                    console.log(response);
                })
                .catch(function (error) {       // ERROR 
                    console.error(error);
                });
}

export function init_listener() {
    // BUTTON - Save SettingsGroup
    $("body").on("click", ".submit-setting-form", function () {
        let setting_form = $(this).closest(".settings-form");
        let form_key = $(setting_form).attr("setting-form-key");
        let data = get_setting_form_data(setting_form)
        // generate endpoint url
        let url = [config.settings_endpoint, 'f', form_key].join("/");
        // sending requeset
        window.flasky_settings.send_form_data(url, data)
    });

}

init_listener()