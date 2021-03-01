<?php
function getComment($conn){
    $query = "SELECT messages, blue, green, red, yellow, white FROM username";
    $result = $conn->query($query);
    if ($result === false){
        echo "<p>" . "DBerror :" . mysqli_error($conn) . "</p>";
    }
    /* fetch object array */
    while ($row = $result->fetch_row()) {
        echo '<div class="commentdiv2">
        <div class="commentdiv3">
            <div class="party">
                <div><img src="img/blue.png"/>'.$row[1].'%</div>
                <div><img src="img/green.png"/>'.$row[2].'%</div>
                <div><img src="img/red.png"/>'.$row[3].'%</div>
                <div><img src="img/yellow.png"/>'.$row[4].'%</div>
                <div><img src="img/white.png"/>'.$row[5].'%</div>
            </div>
            <div class="like">
                <button style="background-image: url(\'img/like.png\');"></button>
                <button style="background-image: url(\'img/dislike.png\');"></button>
            </div>
        </div>
        <div class="text"><p>'.$row[0].'</p></div></div>';
    }
    /* free result set */
    $result->close();
}
?>