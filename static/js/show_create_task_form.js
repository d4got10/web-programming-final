    const showFormBtn = document.getElementById("show-form-btn");
    const myForm = document.getElementById("new_task_form");

    const form_by_type = new Map(
        [
            ["single", document.getElementById("new_task_form_single")],
            ["multiple", document.getElementById("new_task_form_multiple")],
            ["text", document.getElementById("new_task_form_text")]
        ]
    )
    const task_type_btns = document.getElementsByClassName("task_type_btn");

    Array.from(task_type_btns).forEach(element => {
        if(element.checked){
            form_by_type.get(element.value).style.display = "block";
        }
        element.addEventListener('change', function () {
            form_by_type.forEach((value, key, map) => {
                console.log(value);
                console.log(key);
                value.style.display = "none";
            });
            //console.log(element)
            //console.log(form_by_type[element.value])
            form_by_type.get(element.value).style.display = "block";
        })
    })

    showFormBtn.addEventListener("click", () => {
        myForm.style.display = "block";
    });

    /*    myForm.addEventListener("submit", (event) => {
          event.preventDefault(); // Отменяем стандартное поведение формы при отправке
          myForm.style.display = "none";
        });*/
