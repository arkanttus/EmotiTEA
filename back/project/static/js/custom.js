document.addEventListener("DOMContentLoaded", (function() {

    var simpleBarElement = document.getElementsByClassName("js-simplebar")[0];
  
    if(simpleBarElement){
        new ii(document.getElementsByClassName("js-simplebar")[0]);

        var sidebarElement = document.getElementsByClassName("sidebar")[0];
        var sidebarToggleElement = document.getElementsByClassName("sidebar-toggle")[0];
        var overlayElement = document.getElementsByClassName('overlay')[0]
    

        function transitSidebar(){
            sidebarElement.addEventListener("transitionend", function() {
                window.dispatchEvent(new Event("resize"));
            });
        }
        function openSidebar ()  {
            sidebarElement.classList.remove("collapsed")
            overlayElement.classList.replace('invisible', 'visible')
            transitSidebar()
        }  
        function closeSidebar ()  {
            sidebarElement.classList.add("collapsed")
            overlayElement.classList.replace('visible', 'invisible')
            transitSidebar()
        }

        sidebarToggleElement.addEventListener("click", function(){
            openSidebar()
        });

        overlayElement.addEventListener('click', function() {
            closeSidebar()
        });
    }

}));

document.addEventListener("DOMContentLoaded",(function(){
    if(document.getElementsByClassName("js-simplebar")[0]){
        new ii(document.getElementsByClassName("js-simplebar")[0]);
        var e=document.getElementsByClassName("sidebar")[0];
        document.getElementsByClassName("sidebar-toggle")[0].addEventListener("click",(function(){
            e.classList.toggle("collapsed"),
            e.addEventListener("transitionend",(function(){
                window.dispatchEvent(new Event("resize"))
            }
            )
            )
        }
        )
        )
    }
}
)
);
