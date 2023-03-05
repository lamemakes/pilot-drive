/*  This is where all "views" should be populated. For each view, there 
    should be a corresponding icon in src/assets/icons/, and a component 
    in src/views/ with and uppercase first letter.

    Ex: the "media" route has an icon at src/assets/icons/media.svg, and
        a view at src/views/Media.vue.
*/

type route = {
    name: string,
    conditional?: boolean
}

export const routes: route[] = [
    {
        name: "media",
    }, 
    {
        name: "vehicle",
        conditional: true
    },
    {   
        name: "phone",
        conditional: true
    },
    {   
        name: "settings",
    }
];

// Specifify the default route
export const home = routes[1];