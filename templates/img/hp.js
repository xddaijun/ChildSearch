if(!ask) {
    var ask = {};
}

 if(!ask.kids) {
    ask.kids = {};
}

ask.kids.hp = {};

//channel definition
ask.kids.hp.chDef = {
    c_sch : { clickId : 43940, type: 1, qsrc: 0, dest : "schoolhouse"},//cat
    c_mov : { clickId : 43930, type: 2, qsrc: 0, dest : "movies"},//cat, query
    c_vdg : { clickId : 43924, type: 1, qsrc: 0, dest : "games"},//cat
    c_vid : { clickId : 43461, type: 0, qsrc: 0, dest : "video"},
    c_ask : { clickId : 44268, type: 3, qsrc: 0, dest : "http://www.ask.com/web?q={0}"},
    c_img : { clickId : 43466, type: 0, qsrc: 0, dest : "pictures"},
    c_web : { clickId : 43652, type: 0, qsrc: 0, dest : "web"}
};

/**
 * Changes the current channel to the specified value. If the new channel is a link, change window location to the new
 * link. If the new channel is a form, update the channel selection using DHTML
 *
 * @param id new channel id
 * @param li anchor element that was clicked
 *
 */
ask.kids.hp.ch = function(id,li) {
    var query = document.getElementById('q').value;

    _channel = id;

    if(ask.kids.hp.chDef['c_'+id]['type'] == 3) {
        var loc = ask.kids.hp.chDef['c_'+id]['dest'];
        loc = loc.replace("{0}", query);
        loc = loc + _urlSuffix;
        li.href = loc;
        ct(li, ask.kids.hp.chDef['c_'+id]['clickId']); //log click as click thru
        window.location = li.href;
        return false;
    }
    //if query exists, go search channel with query
    if (query != '') {
        if(ask.kids.hp.chDef['c_'+id]['type'] == 0 || ask.kids.hp.chDef['c_'+id]['type'] == 2) {
            li.href = ask.kids._urlPrefixResults + ask.kids.hp.chDef['c_'+id]['dest'] + "?q=" + query + "&qsrc="+  ask.kids.hp.chDef['c_'+id]['qsrc'];
            if (ask.kids.hp.chDef['c_'+id]['type'] == 2) {//cat, append pseudo-channel
                li.href += "&pch=" + id;
            }
            ct(li, ask.kids.hp.chDef['c_'+id]['clickId']); //log click as click thru
            window.location = li.href;
            return false;
        }
    }
    else {
        ct(li, ask.kids.hp.chDef['c_'+id]['clickId']); //log click as click thru            
    }

    //log click
    //sct(ask.kids.hp.chDef['c_'+id]['clickId']);

}