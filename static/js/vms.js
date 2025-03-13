$(document).ready(function(){
    let selectedType = "windows";

    // Handle tab switching
    $(".vm-tab").click(function(){
        $(".vm-tab").removeClass("active");
        $(this).addClass("active");
        selectedType = $(this).data("type");
    });

    // Handle VM creation
    $("#create-vm-btn").click(function(){
        $.ajax({
            url: "/create_vm",
            method: "POST",
            contentType: "application/json",
            data: JSON.stringify({type: selectedType}),
            success: function(response){
                if(response.status === "success"){
                    alert(selectedType.charAt(0).toUpperCase() + selectedType.slice(1) + " VM created!");
                    // Reload the page to update the VM list
                    location.reload();
                } else {
                    alert("Error creating VM: " + response.message);
                }
            },
            error: function(){
                alert("Error creating VM.");
            }
        });
    });
});
