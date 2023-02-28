const TempusDominus = window.tempusDominus.TempusDominus
window.flasky_settings = {}

// loading config
export const config = Object.freeze({
    settings_endpoint: document.querySelector('meta[name="flasky-settings-entpoint"]').content.replace(/\/+$/, '')    // url for the flasky-settings endpoint
});

var mobile_view = false;

// init datetime element
let datetime_element_list = {}
window.datetime_elements = datetime_element_list

$('.init-datetime').each(function(){
    let element = $(this).get(0)
    let td
    let type = $(this).closest("[setting-type]").attr("setting-type")
    switch(type){
        case "datetime":
            td = new TempusDominus(element, {
                display: {
                    sideBySide: true
                }, 
            });
            break
        case "date":
            td = new TempusDominus(element, {
                display: {
                    components: {
                        clock: false
                    }
                },
            });
            break
    }


    datetime_element_list[element] = td
}).get()

function update_date_option(options){
    if(!datetime_element_list){
        return
    } 
    Object.values(datetime_element_list).forEach(_element => {
        _element.updateOptions(options)
    });
}


// window resize funtion

function updateWindowSize() {
    if(window.innerWidth > 600 && mobile_view == true){     // DESKTOP 
        mobile_view = false
        update_date_option({
            display: {
                sideBySide: true
            }
        })
    } else if (window.innerWidth <= 600 && mobile_view == false){   // MOBILE 
        mobile_view = true
        update_date_option({
            display: {
                sideBySide: false
            }
        })
    }
}

window.addEventListener('resize', updateWindowSize)
updateWindowSize()

