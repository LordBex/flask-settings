import {config} from '../init.js'
import * as ElementParser from './element_parser.js'

const html_element = $('settings_meta')

// set state functions 

function set_changes_on_group(setting_group){
    $(setting_group).attr('has-changes', '')
}

function remove_changes_on_group(setting_group){
    $(setting_group).removeAttr('has-changes', '')
}


// get information functions 

function get_setting_group_data(setting_group){
    let data = {};
    $(setting_group)
        .find(".settings-element")
        .each(function () {
            let [element_key, element_value] = ElementParser.parse_element(this)
            data[element_key] = element_value
        });
    return data
}

// init functions

export function init_listener() {
    // BUTTON - Save SettingsGroup
    $("body").on("click", ".btn-setting-save", function () {
        let settings_group = $(this).closest(".settings-group");
        let settings_key = $(settings_group).attr("setting-group-key");
        let data = get_setting_group_data(settings_group)
        // generate endpoint url
        let url = [config.settings_endpoint, 's', settings_key, "set"].join("/");
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
                remove_changes_on_group(settings_group)
            })
            .catch(function (error) {       // ERROR 
                console.error(error);
            });
    });

    // BUTTON - SettingGroup - OnChanges -> set has-changes Badge
    $("body").on('change', ".observed-input", function () {
        let settings_group = $(this).closest(".settings-group");
        set_changes_on_group(settings_group)
    });
}
