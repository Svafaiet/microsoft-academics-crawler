function main(splash, args)
    local max_waits = 15
    local delay = 2
    assert(splash:go(splash.args.url))

    for _ = 1, max_waits do
        splash:wait(delay)
        if splash:select("#mainArea > router-view > div > div > div > div > h1.name")
            and splash:select("#mainArea > router-view > div > div > div > div > div.stats > ma-statistics-item:nth-child(1) > div.ma-statistics-item.au-target > div.data > div.count")
            and splash:select("#mainArea > router-view > div > div > div > div > div.stats > ma-statistics-item:nth-child(2) > div.ma-statistics-item.au-target > div.data > div.count")
            and splash:select("#mainArea > router-view > div > div > div > div > p") then

        else
            ::continue::
        end
        local show_more = splash:select('#mainArea > router-view > div > div > div > div > div.topics > ma-tag-cloud > div > div[aria-expanded="false"]')
        if show_more then
            show_more:click()
            ::continue::
      	end
        local show_less = splash:select('#mainArea > router-view > div > div > div > div > div.topics > ma-tag-cloud > div > div[aria-expanded="true"]')
        if show_more == nil and show_less == nil then
            ::continue::
        end
        if splash:select("#mainArea > router-view > router-view > ma-edp-serp > div > div.results > div > compose > div > div.results > ma-card:nth-child(2) > div > compose > div > div.primary_paper > a.title.au-target") then
            break
        end


    end


    return {
        png = splash:png(),
        html = splash:html(),
        har = splash:har()
       }
end