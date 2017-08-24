(function($) {
    "use strict";

    $(document).on('ready', function() {
        $('.get_comments').on('click', function(e) {
            $.post('/posts/get_comments?id=' + e.target.id, function(data) {
                debugger
                $('#exampleModalLong').html(data);
            }, 'html');
        });
        var $window = $(window),
            $body = $('body'),
            $document = $(document),
            drew = {
                headerFloatingHeight: 60,
            };

        /**
         * =======================================
         * Function: Detect Mobile Device
         * =======================================
         */
        // source: http://www.abeautifulsite.net/detecting-mobile-devices-with-javascript/
        var isMobile = {
            Android: function() {
                return navigator.userAgent.match(/Android/i);
            },
            BlackBerry: function() {
                return navigator.userAgent.match(/BlackBerry/i);
            },
            iOS: function() {
                return navigator.userAgent.match(/iPhone|iPad|iPod/i);
            },
            Opera: function() {
                return navigator.userAgent.match(/Opera Mini/i);
            },
            Windows: function() {
                return navigator.userAgent.match(/IEMobile/i);
            },
            any: function() {
                return (isMobile.Android() || isMobile.BlackBerry() || isMobile.iOS() || isMobile.Opera() || isMobile.Windows());
            },
        };

        /**
         * =======================================
         * Function: Resize Background
         * =======================================
         */
        var resizeBackground = function() {

            $('.section-background-video > video, .section-background-image > img, .two-cols-description-image > img').each(function(i, el) {

                var $el = $(el),
                    $section = $el.parent(),
                    min_w = 300,
                    el_w = el.tagName == 'VIDEO' ? el.videoWidth : el.naturalWidth,
                    el_h = el.tagName == 'VIDEO' ? el.videoHeight : el.naturalHeight,
                    section_w = $section.outerWidth(),
                    section_h = $section.outerHeight(),
                    scale_w = section_w / el_w,
                    scale_h = section_h / el_h,
                    scale = scale_w > scale_h ? scale_w : scale_h,
                    new_el_w, new_el_h, offet_top, offet_left;

                if (scale * el_w < min_w) {
                    scale = min_w / el_w;
                };

                new_el_w = scale * el_w;
                new_el_h = scale * el_h;
                offet_left = (new_el_w - section_w) / 2 * -1;
                offet_top = (new_el_h - section_h) / 2 * -1;

                $el.css('width', new_el_w);
                $el.css('height', new_el_h);
                $el.css('marginTop', offet_top);
                $el.css('marginLeft', offet_left);
            });

        };
        $body.on('pageStart', function() {
            resizeBackground();
        });

        /**
         * =======================================
         * IE9 Placeholder
         * =======================================
         */
        $('#form-choose-app').on('submit', function() {
            var form = $(this);
            $.ajax({
                type: 'POST',
                data: form.serialize(), //username and password
                url: form.attr('action'),
                contentType: "application/x-www-form-urlencoded; charset=UTF-8",
                success: function(response) {
                    if (response['success'] == true) {
                        window.location = window.location;
                    } else {
                        alert('Something broke. Let us pray this is not mid-interview!');
                    }
                },
                error: function(xhr) {
                    alert('failed')
                }
            });
            return false;
        });

        $("#quick-post").on('submit', function(e) {
            debugger
            e.preventDefault(); // don't submit multiple times
            this.submit(); // use the native submit method of the form element
            var input = $('#message-box');
            input.val("");
            var input = $('#img-upload');
            input.val("");
            $(".img-preview").attr('src', "");
        });
        /**
         * =======================================
         * Detect Mobile Device
         * =======================================
         */
        if (isMobile.any()) {
            // add identifier class to <body>
            $body.addClass('mobile-device');
            // remove all element with class "remove-on-mobile-device"
            $('.remove-on-mobile-device').remove();
        };

        /* =======================================
         * Resize Video Background
         * =======================================
         */
        $window.on('resize', function() {
            resizeBackground();
        });

        /* =======================================
         * Slideshow Background
         * =======================================
         */
        if ($.fn.responsiveSlides) {
            $body.on('pageStart', function() {
                $('.section-background-slideshow').responsiveSlides({
                    speed: $(this).data('speed') ? $(this).data('speed') : 800,
                    timeout: $(this).data('timeout') ? $(this).data('timeout') : 4000,
                });
            });
        };

        /* =======================================
         * Testimonial Slider
         * =======================================
         */
        if ($.fn.responsiveSlides) {
            $body.on('pageStart', function() {
                $('.testimonial-slider').responsiveSlides({
                    speed: $(this).data('speed') ? $(this).data('speed') : 800,
                    timeout: $(this).data('timeout') ? $(this).data('timeout') : 4000,
                    auto: $(this).data('auto') ? $(this).data('auto') : false,
                    pager: true,
                });
            });
        };

        /* =======================================
         * Hero Slider
         * =======================================
         */
        if ($.fn.responsiveSlides) {
            $body.on('pageStart', function() {
                $('.section-slider').responsiveSlides({
                    speed: $(this).data('speed') ? $(this).data('speed') : 800,
                    timeout: $(this).data('timeout') ? $(this).data('timeout') : 4000,
                    auto: $(this).data('auto') ? $(this).data('auto') : false,
                    nav: true,
                });
            });
        };

        /**
         * =======================================
         * Initiate Stellar JS
         * =======================================
         */
        if ($.fn.stellar && !isMobile.any()) {
            $.stellar({
                responsive: true,
                horizontalScrolling: false,
                hideDistantElements: false,
                verticalOffset: 0,
                horizontalOffset: 0,
            });
        };
        /**
         * =======================================
         * Scroll Spy
         * =======================================
         */
        var toggleHeaderFloating = function() {
            // Floating Header
            if ($window.scrollTop() > 80) {
                $('.header-section').addClass('floating');
            } else {
                $('.header-section').removeClass('floating');
            };
        };

        $window.on('scroll', toggleHeaderFloating);

        /**
         * =======================================
         * One Page Navigation
         * =======================================
         */
        if ($.fn.onePageNav) {
            $('#header-nav').onePageNav({
                scrollSpeed: 1000,
                filter: ':not(.external)',
                begin: function() {
                    $('#navigation').collapse('toggle');
                },
            });
        };

        /**
         * =======================================
         * Animations
         * =======================================
         */
        if ($body.hasClass('enable-animations') && !isMobile.any()) {
            var $elements = $('*[data-animation]');

            $elements.each(function(i, el) {

                var $el = $(el),
                    animationClass = $el.data('animation');

                $el.addClass(animationClass);
                $el.addClass('animated');
                $el.addClass('wait-animation');

                $el.one('inview', function() {
                    $el.removeClass('wait-animation');
                    $el.addClass('done-animation');
                });
            });
        };

        /**
         * =======================================
         * Anchor Link
         * =======================================
         */
        $body.on('click', 'a.anchor-link', function(e) {
            e.preventDefault();

            var $a = $(this),
                $target = $($a.attr('href'));

            if ($target.length < 1) return;

            $('html, body').animate({ scrollTop: Math.max(0, $target.offset().top - drew.headerFloatingHeight) }, 1000);
        });

        /**
         * =======================================
         * Form AJAX
         * =======================================
         */
        $('form').each(function(i, el) {

            var $el = $(this);

            if ($el.hasClass('form-ajax-submit')) {

                $el.on('submit', function(e) {
                    e.preventDefault();

                    var $alert = $el.find('.form-validation'),
                        $submit = $el.find('button'),
                        action = $el.attr('action');

                    // button loading
                    $submit.button('loading');

                    // reset alert
                    $alert.removeClass('alert-danger alert-success');
                    $alert.html('');

                    $.ajax({
                        type: 'POST',
                        url: action,
                        data: $el.serialize() + '&ajax=1',
                        dataType: 'JSON',
                        success: function(response) {

                            // custom callback
                            $el.trigger('form-ajax-response', response);

                            // error
                            if (response.error) {
                                $alert.html(response.message);
                                $alert.addClass('alert-danger').fadeIn(500);
                            }
                            // success
                            else {
                                $el.trigger('reset');
                                $alert.html(response.message);
                                $alert.addClass('alert-success').fadeIn(500);
                            }

                            // reset button
                            $submit.button('reset');
                        },
                    })
                });
            };
        });
        $('#date_clear').on('click', function(e) {
            $('.date').datepicker('setDate', null);
        });

        /* =======================================
         * Preloader
         * =======================================
         */
        if ($.fn.jpreLoader && $body.hasClass('enable-preloader')) {

            $body.on('pageStart', function() {
                $body.addClass('done-preloader');
            });

            $body.jpreLoader({
                showSplash: false,
                // autoClose : false,
            }, function() {
                $body.trigger('pageStart');
            });

        } else {
            $body.trigger('pageStart');
        };

        $window.trigger('resize');
        $window.trigger('scroll');

    });
    $("#img-upload").on("change", function(e) {
        $(".img-preview").fadeIn("fast").attr('src', URL.createObjectURL(event.target.files[0]))
    });

    $('#num_posts').on('change', function(e) {
        // debugger
        var new_loc = String(window.location.origin) + "/" + this.value;
        window.location = new_loc;
    });



    var bindDatePicker = function() {
        $(".date").datetimepicker({
            format: 'DD/MM/YYYY HH:mm',
            icons: {
                time: "fa fa-clock-o",
                date: "fa fa-calendar",
                up: "fa fa-arrow-up",
                down: "fa fa-arrow-down"
            }
        }).find('input:first').on("blur", function() {
            // check if the date is correct. We can accept dd-mm-yyyy and yyyy-mm-dd.
            // update the format if it's yyyy-mm-dd
            var date = parseDate($(this).val());

            if (!isValidDate(date)) {
                //create date based on momentjs (we have that)
                date = moment().format('DD/MM/YYYY HH:mm');
            }

            $(this).val(date);
        });
    }

    var isValidDate = function(value, format) {
        format = format || false;
        // lets parse the date to the best of our knowledge
        if (format) {
            value = parseDate(value);
        }

        var timestamp = Date.parse(value);

        return isNaN(timestamp) == false;
    }

    var parseDate = function(value) {
        // var m = value.match(/^(\d{1,2})(\/|-)?(\d{1,2})(\/|-)?(\d{4})$/);
        // if (m)
        //     value = m[5] + '-' + ("00" + m[3]).slice(-2) + '-' + ("00" + m[1]).slice(-2);

        return value;
    }

    bindDatePicker();


})(jQuery);