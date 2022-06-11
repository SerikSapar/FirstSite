$('#groups').on('submit', function (e) {
        e.preventDefault()
        $.ajax({
            type: 'POST',
            url: '',
            data: $(this).serialize(),
        })
    })
