import mediaIcon from '../assets/icons/media.svg'
import vehicleIcon from '../assets/icons/vehicle.svg'
import phoneIcon from '../assets/icons/phone.svg'
import settingsIcon from '../assets/icons/settings.svg'

/*  This is where all "views" should be populated. For each view, there 
    should be a corresponding icon in src/assets/icons/, and a component 
    in src/views/ with and uppercase first letter.

    Ex: the "media" route has an icon at src/assets/icons/media.svg, and
        a view at src/views/Media.vue.
*/

export interface route {
    name: string,
    icon: string,
    conditional: boolean,
}

export const routes: route[] = [
    {
        name: "media",
        icon: mediaIcon,
        conditional: false
    }, 
    {
        name: "vehicle",
        icon: vehicleIcon,
        conditional: true
    },
    {   
        name: "phone",
        icon: phoneIcon,
        conditional: true
    },
    {   
        name: "settings",
        icon: settingsIcon,
        conditional: false
    }
];

// Specifify the default route
export const home = routes[1];