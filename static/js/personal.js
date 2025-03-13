$(document).ready(function(){
    function fetchStats(){
        $.ajax({
            url: "/stats",
            method: "GET",
            success: function(data){
                let statusHtml = `
                    <span><strong>Time:</strong> ${data.time}</span>
                    <span><strong>Battery:</strong> ${data.battery !== "N/A" ? data.battery + "%" : "N/A"}</span>
                    <span><strong>CPU:</strong> ${data.cpu}%</span>
                    <span><strong>RAM:</strong> ${ (data.memory.used / (1024*1024)).toFixed(2) } MB / ${ (data.memory.total / (1024*1024)).toFixed(2) } MB</span>
                    <span><strong>GPU:</strong> ${data.gpu !== "N/A" ? (typeof data.gpu === 'number' ? data.gpu.toFixed(2) + "%" : data.gpu) : "N/A"}</span>
                `;
                $("#status-bar").html(statusHtml);
            },
            error: function(){
                $("#status-bar").html("<p>Error loading system stats.</p>");
            }
        });
    }

    // Initial stats update and then every 5 seconds
    fetchStats();
    setInterval(fetchStats, 5000);

    // Toggle remote control overlay when the screen is clicked
    $(".screen").click(function(){
        $("#remote-control-overlay").fadeIn();
    });

    $("#close-remote").click(function(){
        $("#remote-control-overlay").fadeOut();
    });
});
