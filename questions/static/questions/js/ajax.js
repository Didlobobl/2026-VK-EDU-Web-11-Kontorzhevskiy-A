$(document).ready(function() {
    
    $('.like-btn, .dislike-btn').click(function(e) {
        e.preventDefault();
        const btn = $(this);
        const objId = btn.data('id');
        const objType = btn.data('type');
        
        let action = btn.data('action');
        if (!action) {
            action = btn.hasClass('like-btn') ? 'like' : 'dislike';
        }

        $.ajax({
            url: VOTE_URL,
            method: 'POST',
            data: {
                'id': objId,
                'type': objType,
                'action': action,
                'csrfmiddlewaretoken': CSRF_TOKEN
            },
            success: function(response) {
                const counterId = '#rating-' + objType + '-' + objId;
        
            $(counterId).text(response.new_rating);
        
            btn.closest('.btn-group-vote').find('.like-btn, .dislike-btn').removeClass('active');
            if (response.is_active) {
                btn.addClass('active');
            }
            },  
            error: function(xhr) {
                if (xhr.status === 403) {
                    alert("Войдите в систему, чтобы голосовать.");
                } else {
                    alert("Ошибка при обработке голоса.");
                }
            }
        });
    });

    $(document).on('change', '.correct-checkbox', function() {
        const checkbox = $(this);
        const answerId = checkbox.data('id');

        $.ajax({
            url: MARK_CORRECT_URL, 
            method: 'POST',
            data: {
                'answer_id': answerId,
                'csrfmiddlewaretoken': CSRF_TOKEN
            },
            success: function(response) {
                if (response.status === 'ok') {
                    $('.card').removeClass('border-success border-4');
                    $('.correct-checkbox').not(checkbox).prop('checked', false);
                    
                    if (checkbox.is(':checked')) {
                        checkbox.closest('.card').addClass('border-success border-4');
                    }
                }
            },
            error: function(xhr) {
                checkbox.prop('checked', !checkbox.prop('checked'));
                alert(xhr.responseJSON.message || "Ошибка доступа.");
            }
        });
    });
});