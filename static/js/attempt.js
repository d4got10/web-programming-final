    const elements = document.getElementsByClassName("readonly");
    for (let i = 0; i < elements.length; i++) {
        const element = elements.item(i);
        element.readOnly = true;
    }

    const countDownDate = new Date("{{ attempt.end_date }}").getTime();

    const update_time = function () {

        var now = new Date().getTime();

        var distance = countDownDate - now;

        var days = Math.floor(distance / (1000 * 60 * 60 * 24));
        var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        var seconds = Math.floor((distance % (1000 * 60)) / 1000);

        document.getElementById("timer").innerHTML = "Осталось: " + days + "д " + hours + "ч "
            + minutes + "м " + seconds + "с ";

        if (distance < 0) {
            clearInterval(x);
            document.getElementById("timer").innerHTML = "Завершено";
        }
    }

    update_time()
    // Update the count down every 1 second
    const x = setInterval(update_time, 1000);