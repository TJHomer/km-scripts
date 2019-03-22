<?php
//require("common.php"); Contains hdbcall - a function common to all the mattermost bots used by knoxmakers

function hdbcall ($call, $data){
        $data = json_encode($data);
        $url = "https://haxdb-api.knoxmakers.org/v1/".$call;
        $ch = curl_init($url);
        curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "POST");
        curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_HTTPHEADER, array(
            'Content-Type: application/json',
            'Content-Length: ' . strlen($data))
        );
        $result = curl_exec($ch);
        return json_decode($result, true);
}




$apikey = "your-key";


$_HOOK = "your-mattermost-hook";




$output = Array();

$today = date("Y-m-d");
$query = "PEOPLE_UDF4=$today"; #date trial is up

$r = hdbcall("PEOPLE/list", array("api_key" => $apikey, "query" => $query));

$count = ($r["data"]);


foreach($count as $value) {
    $output["channel"] = "channel"; 
    $output["username"] = "bot";
    $output["icon_url"] = "icon.png";
    $txt = "# VOTE PLS with :thumbsup:";


    $row = $value;
    $output["text"] = $txt;
    $output["attachments"] = array(
        array(
            "color" => "#FF0000",
            "pretext" => "",
            "text" => "",
            "fields" => array(
                array(
                    "short" => false,
                    "title" => "NAME",
                    "value" => "` ".$row["ROWNAME"]." `"
                ),
                array(
                    "short" => true,
                    "title" => "EMAIL",
                    "value" => "` ".$row["PEOPLE_EMAIL"]." `"
                ),
                array(
                    "short" => true,
                    "title" => "MATTERMOST",
                    "value" => "` ".$row["PEOPLE_UDF11"]." `" #mattermost handle
                ),
                array(
                    "short" => true,
                    "title" => "TRIAL ENDS",
	            "value" => "` ".$row["PEOPLE_UDF4"]." `"
		),
                array(
                     "short" => true,
                     "title" => "Intent information",
                     "value" => "` ".$row["PEOPLE_UDF5"]." `"  #personal bio
                ),
            ),
        )
    );
        $r = hdbcall("THUMBNAILS/get", array("api_key" => $apikey, "context" => "PEOPLE", "contextid" => $row["ROWID"]));
        if ($r["success"] == 1){
                list($blah, $img) = explode(",", $r["data"]);
                $img = str_replace(" ", "+", $img);
                $img = base64_decode($img);
                $filepath = "path";
                $file = "thumbs/".uniqid().".jpg";
                file_put_contents($filepath.$file, $img);
                $output["attachments"][0]["image_url"] = "$filepath,$file";

        }

        json_post($_HOOK, $output);

}
exit();
?>


