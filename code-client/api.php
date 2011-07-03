<?php 
// PHP简易中文分词(SCWS) 第4版 API 
// 2010/12/01 
// $Id: $ 
// 
set_time_limit(0); 
error_reporting(0); 
ini_set('display_errors', '0'); 

// show source 
if (isset($_SERVER['QUERY_STRING'])  
    && !strncasecmp($_SERVER['QUERY_STRING'], 'source', 6)) 
{ 
    highlight_file(__FILE__); 
    exit(0); 
} 

// get data 
if (!isset($_POST['data'])) 
{ 
    $charset = 'utf-8'; 
    $respond = 'plain'; 
    $apiurl = 'http://' . $_SERVER['HTTP_HOST'] . $_SERVER['SCRIPT_NAME'];     
} 
$data = trim($_POST['data']); 

// get respond 
$respond = isset($_POST['respond']) ? strtolower($_POST['respond']) : 'php'; 
if ($respond === 'json' && !function_exists('json_encode')) 
{ 
    $respond = 'plain'; 
    $result = '{"status":"error","message":"JSON data is unavailable"}'; 
    output_result($result); 
} 
if ($respond !== 'php' && $respond !== 'json' && $respond !== 'xml') 
{ 
    $respond = 'php'; 
    output_result(set_simple_result('Invalid parameter: respond')); 
} 

// get charset 
$charset = (isset($_POST['charset']) ? strtolower($_POST['charset']) : 'utf8'); 
if ($charset === 'utf-8') $charset = 'utf8'; 
else if ($charset === 'gb2312' || $charset === 'gb18030') $charset = 'gbk'; 
if ($charset !== 'gbk' && $charset !== 'utf8') 
    output_result(set_simple_result('Invalid parameter: charset')); 
if ($charset !== 'utf8' && $respond == 'json') 
    output_result(set_simple_result('JSON respond data only work with utf8 charset')); 

// get other parameters 
$ignore = (isset($_POST['ignore']) && !strcasecmp($_POST['ignore'], 'yes')) ? true : false; 
$duality = (isset($_POST['duality']) && !strcasecmp($_POST['duality'], 'yes')) ? true : false; 
$traditional = (isset($_POST['traditional']) && !strcasecmp($_POST['traditional'], 'yes')) ? true : false; 
$multi = isset($_POST['duality']) ? intval($_POST['duality']) : 0; 
if ($multi < 0 || $multi > 15) 
    output_result(set_simple_result('Invalid parameter: multi')); 

// do segmentation 
$scws = scws_new(); 
$scws->set_charset($charset); 
if ($charset === 'utf8' && $traditional === true) 
{ 
    $scws->set_rule(ini_get('scws.default.fpath') . '/rules_cht.utf8.ini'); 
    $scws->set_dict(ini_get('scws.default.fpath') . '/dict_cht.utf8.xdb'); 
} 

    $scws->add_dict('/home/game.txt',SCWS_XDICT_TXT);
    $scws->add_dict('/home/movie.txt',SCWS_XDICT_TXT);
// apply other settings & send the text content 
$scws->set_duality($duality); 
$scws->set_ignore($ignore); 
$scws->set_multi($multi); 
$scws->send_text($data); 

// fetch the result 
$words = array(); 
while ($res = $scws->get_result()) $words = array_merge($words, $res); 

// output the result 
$result = array('status' => 'ok', 'words' => $words); 
output_result($result); 

// ----------------------------------------------------------------- 
// internal functions 
// ----------------------------------------------------------------- 
// output real result 
function output_result($result) 
{ 
    global $respond, $scws, $charset; 
    if ($scws) $scws->close(); 

    // get oe (output encoding) 
    if ($charset === 'utf8') $charset = 'utf-8';     
    // header 
    if ($respond === 'xml') 
    { 
        header('Content-Type: text/xml; charset=' . $charset); 
        echo '<?xml version="1.0" encoding="' . $charset . '"?>' . "\n"; 
        echo array_to_xml($result, '', 'respond'); 
    } 
    else 
    { 
        header('Content-Type: text/plain; charset=' . $charset); 
        if ($respond === 'json') 
            echo json_encode($result); 
        else if ($respond === 'php') 
            echo serialize($result); 
        else 
            echo $result; 
    } 
    exit(0); 
} 

// set error 
function set_simple_result($msg = 'Unknown reason', $type = 'error') 
{ 
    return array('status' => $type, 'message' => $msg); 
} 

// convert php array to xml 
function array_to_xml($var, $tag = '', $type = 'respond') 
{ 
    if (!is_int($type)) 
    { 
        if ($tag) return array_to_xml(array($tag => $var), 'scws:' . $type, 0); 
        else 
        { 
            $tag = 'scws:' . $type; 
            $type = 0; 
        } 
    }     
    $level = $type; 
    $indent = str_repeat("\t", $level); 
    if (!is_array($var)) 
    { 
        $ret .= $indent . '<' . $tag; 
        $var = strval($var); 
        if ($var == '') $ret .= ' />'; 
        else if (!preg_match('/[^0-9a-zA-Z@\._:\/-]/', $var)) $ret .= '>' . $var . '</' . $tag . '>'; 
        else if (strpos($var, "\n") === false) $ret .= '><![CDATA[' . $var . ']]></' . $tag . '>'; 
        else $ret .= ">\n{$indent}\t<![CDATA[{$var}]]>\n{$indent}</{$tag}>"; 
        $ret .= "\n"; 
    } 
    else if (_is_simple_array($var)) 
    {             
        foreach ($var as $tmp) $ret .= array_to_xml($tmp, $tag, $level); 
    } 
    else 
    { 
        $ret .= $indent . '<' . $tag; 
        if ($level == 0) $ret .= ' xmlns:scws="http://www.ftphp.com/scws"'; 
        $ret .= ">\n"; 
        foreach ($var as $key => $val) 
        { 
            $ret .= array_to_xml($val, $key, $level + 1); 
        } 
        $ret .= "{$indent}</{$tag}>\n"; 
    } 
    return $ret; 
} 

// check an array is hash-related array or not 
function _is_simple_array($arr) 
{ 
    $i = 0; 
    foreach ($arr as $k => $v) { if ($k !== $i++) return false; } 
    return true; 
} 
