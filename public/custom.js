$(function () {

    $('.social a').on('click', function (e) {

        e.preventDefault();

        window.open($(this).attr('href'), 'shareWindow', 'height=450, width=600, top=' + ($(window).height() / 2 - 275) + ', left=' + ($(window).width() / 2 - 300) + ', toolbar=0, location=0, menubar=0, directories=0, scrollbars=0');


    });
});