/////////////////////////////////////////////
// Загрузка
$(document).ready(function () {
    var active_page = location.href.split("/").slice(-1);
    console.log("active_page: '" + active_page + "'");

    // Меню на каждой странице
    if (active_page != "login.html")
        include_navigation_html();

    // Скрытие Alert
    // document.getElementById('alert').style.display = 'none';
    $("#alert").css("display", "none");

    // onload страниц
    if (active_page == "login.html")
        login_page_onload();
    if (active_page == "info.html")
        info_page_onload();
    if (active_page == "settings.html")
        settings_page_onload();
    if (active_page == "work_model.html")
        work_model_page_onload();
    if (active_page == "employees.html")
        employees_page_onload();
});

// Меню на каждой странице
function include_navigation_html() {
    console.log("include_navigation_html()");
    var z, i, elmnt, file, xhttp;
    // Loop through a collection of all HTML elements:
    z = document.getElementsByTagName("*");
    for (i = 0; i < z.length; i++) {
        elmnt = z[i];
        // search for elements with a certain atrribute:
        file = elmnt.getAttribute("include-navigation-html");
        if (file) {
            // Make an HTTP request using the attribute value as the file name:
            xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function () {
                if (this.readyState == 4) {
                    if (this.status == 200) {
                        elmnt.innerHTML = this.responseText;
                        var active_page = location.href.split("/").slice(-1);
                        var menu_html_links = elmnt.querySelector("nav div div ul");
                        var menu_html_elements = menu_html_links.getElementsByTagName("a");
                        for (i = 0; i < menu_html_elements.length; i++) {
                            if (menu_html_elements[i].getAttribute("href") == active_page) {
                                menu_html_elements[i].classList.add("active");
                                break;
                            }
                        }
                    }
                    if (this.status == 404) {
                        elmnt.innerHTML = "Page not found.";
                    }
                    // Remove the attribute, and call this function once more: 
                    elmnt.removeAttribute("include-navigation-html");
                    include_navigation_html();
                }
            };
            xhttp.open("GET", file, true);
            xhttp.send();
            // Exit the function:
            return;
        }
    }
}

function logout() {
    $.post("/api/logout")
        .complete(function () { window.location.replace("login.html") });
}

/////////////////////////////////////////////
// login.html
function login_page_onload() {
}

// Логин по enter на #login_form
$("#login_form input").keypress(function (e) {
    if (e.keyCode == 13) {
        login();
    }
});

// Логин /api/login
function login() {
    var username = document.getElementById("Username").value;
    var passwd = document.getElementById("Password").value;
    console.log("username: " + username + "; passwd: " + "*".repeat(passwd.length));

    /*    $.post("/api/login", JSON.stringify({ "login": username, "password": passwd }))
            .success(function (data) {
                var jsonResponse = JSON.parse(data);
                console.log("Post ok. Got status: " + jsonResponse.status);
                if (jsonResponse.status) {
                    $("#alert").css("display", "none");
                    window.location.replace("info.html");
                } else {
                    console.log("Incorrect Username or Password");
                    $("#alert").css("display", "inherit");
                }
            })
            .error(function () {
                console.log("Incorrect Username or Password");
                $("#alert").css("display", "inherit");
            });
    */
    var url = "/api/login";
    var xhr = new XMLHttpRequest();
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var jsonResponse = JSON.parse(xhr.responseText);
            console.log("jsonResponse.status: " + jsonResponse.status);
            if (jsonResponse.status) {
                document.getElementById('alert').style.display = 'none';
                window.location.replace("info.html");
            } else {
                console.log("Incorrect Username or Password");
                document.getElementById('alert').style.display = 'inherit';
            }
        }
    };
    var data = JSON.stringify({ "login": username, "password": passwd });
    xhr.send(data);
}

/////////////////////////////////////////////
// info.html
function info_page_onload() {
    $.getJSON("/api/deviceinfo", {})
        .success(function (data) {
            console.log("Got data ok: " + data);
        })
        .error(function (error) { 
            console.log("ERROR get data: " + error.error) 
        });
    /*
        $.ajax({
            url: "/api/deviceinfo",
            type: "GET",
            dataType: 'json',
            data: { },
            // contentType: 'application/json; charset=utf-8',
            contentType: 'application/json',
            // headers: {
            //     'sigin': 'true'
            // },
            beforeSend: function(xhr){xhr.setRequestHeader('sigin', 'true');},
            success: function(result) { alert('Success!' + result); },
            error: function (error) { alert('ERROR!' + error.error); }
         });
    */
    /*
        $.ajax({
            url: '/api/deviceinfo',
            type: 'GET',
            dataType: 'json',
            success: function (data) {
                console.log("Got data ok");
                document.getElementById('alert').style.display = 'none';
                document.getElementById('data').style.display = 'inherit';
     
                document.getElementById("serial").innerText = " " + data.serial;
                document.getElementById("software_version").innerText = " " + data.software_version;
                document.getElementById("coproc_version").innerText = " " + data.coproc_version;
                document.getElementById("pvs_version").innerText = " " + data.pvs_version;
                document.getElementById("math_version").innerText = " " + data.math_version;
                document.getElementById("qt_ver").innerText = data.qt_ver;
                document.getElementById("uname").innerText = data.uname;
                document.getElementById("templ_count").innerText = data.templ_count;
                document.getElementById("employee_count").innerText = data.employee_count;
                document.getElementById("ip_term").innerText = data.ip_term;
                document.getElementById("studio_connected").innerText = data.studio_connected;
                document.getElementById("ip_studio").innerText = data.ip_studio;
                document.getElementById("ident_server_connected").innerText = data.ident_server_connected;
            },
            error: function () {
                document.getElementById('alert').style.display = 'inherit';
                document.getElementById('alert').innerHTML = "Request error";
                document.getElementById('data').style.display = 'none';
                window.location.replace("login.html");
            },
            beforeSend: setHeader
        });
    */
}

function setHeader(xhr) {
    // xhr.setRequestHeader('test', 'test');
    // xhr.setRequestHeader('test2', 'test2');
}


/////////////////////////////////////////////
// settings.html
function settings_page_onload() {
}

/////////////////////////////////////////////
// work_model.html
function work_model_page_onload() {
    // xhr.setRequestHeader("Content-Type", "application/json");    
    // xhr.setRequestHeader("sigin", "true");
    // $.getJSON('http://localhost:8081/api/work_model/branches', function (data) {
    //     setRequestHeader("siginnnn", "true");
    //     var branches_list = data.map(branch => `<a href="${branch.name}">${branch.name}</a><br>`),
    //         text = `<h2>Branches</h2><br>${branches_list.join('')}`;
    //     console.log(branches_list);
    //     $(".panel_branches").html(text);
    // });

    $.ajax({
        url: '/api/work_model/branches',
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            //alert('hello!'); 
            var branches_list = data.map(branch => `<a href="${branch.name}">${branch.name}</a><br>`);
            console.log("Got branches_list: " + branches_list)
        },
        error: function () {
            document.getElementById('alert').style.display = 'inherit';
            document.getElementById('alert').innerHTML = "Request error";
        },
        beforeSend: setHeader
    });
}

/////////////////////////////////////////////
// employees.html
function employees_page_onload() {
}

/////////////////////////////////////////////
// metisMenu
$(function () {
    $("#side-menu").metisMenu();
});

// Loads the correct sidebar on window load,
// collapses the sidebar on window resize.
// Sets the min-height of #page-wrapper to window size
$(function () {
    $(window).bind("load resize", function () {
        topOffset = 50;
        width =
            this.window.innerWidth > 0 ? this.window.innerWidth : this.screen.width;
        if (width < 768) {
            $("div.navbar-collapse").addClass("collapse");
            topOffset = 100; // 2-row-menu
        } else {
            $("div.navbar-collapse").removeClass("collapse");
        }

        height =
            (this.window.innerHeight > 0
                ? this.window.innerHeight
                : this.screen.height) - 1;
        height = height - topOffset;
        if (height < 1) height = 1;
        if (height > topOffset) {
            $("#page-wrapper").css("min-height", height + "px");
        }
    });

    var url = window.location;
    var element = $("ul.nav a")
        .filter(function () {
            return this.href == url || url.href.indexOf(this.href) == 0;
        })
        .addClass("active")
        .parent()
        .parent()
        .addClass("in")
        .parent();
    if (element.is("li")) {
        element.addClass("active");
    }
});

/////////////////////////////////////////////
// FUNCIONS
// function newSessionCookie() {
//     var session_id = Math.random().toString(36).substr(2, 9);    
//     return session_id;
// }

// function getCookie(cname) {
//     var name = cname + "=";
//     console.log("document.cookie: " + document.cookie);
//     var ca = document.cookie.split(';');
//     for (var i = 0; i < ca.length; i++) {
//         var c = ca[i];
//         while (c.charAt(0) == ' ')
//             c = c.substring(1);
//         if (c.indexOf(name) != -1)
//             return c.substring(name.length, c.length);
//     }
//     return "";
// }

// function setCookie(name, value, days) {
//     var expires = "";
//     if (days) {
//         var date = new Date();
//         date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
//         expires = "; expires=" + date.toUTCString();
//     }
//     document.cookie = name + "=" + (value || "") + expires + "; path=/";
// }

// function eraseCookie(name) {   
//     document.cookie = name+'=; Max-Age=-99999999;';  
// }
