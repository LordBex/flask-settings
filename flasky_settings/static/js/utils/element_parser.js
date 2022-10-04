
var parsing_functions = {}


export function parse_element(element){
    let type = $(element).attr('setting-type')
    if (type in parsing_functions){
        let key = $(element).attr("settings-element-key");
        let value = parsing_functions[type](element, key)
        return [key, value]
    }
    alert('[Error][SettingsElement] parsing function for "'+ type +'" not exist')
}

export function regist_parsing_function(type, f){
    parsing_functions[type] = f
}

function parse_string_element(element){
    let value = $("input", element).first().val();
    return value
}
regist_parsing_function('string', parse_string_element)

function parse_bool_element(element){
    let value = $("input", element).first().is(":checked");
    return value
}
regist_parsing_function('bool', parse_bool_element)

function parse_multi_select_element(element){
    let value = $('.form-check-input:checked', element).map(function(){
        let v = $(this).parent().text().trim()
        return v
    }).toArray()
    return value
}
regist_parsing_function('multi-select', parse_multi_select_element)

function parse_select_element(element){
    let value = $('select', element).val()
    return value
}
regist_parsing_function('select', parse_select_element)

function parse_text_element(element){
    let value = $('textarea', element).val()
    return value
}
regist_parsing_function('text', parse_text_element)
