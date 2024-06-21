$(document).ready(function () {
    $('.js-btn-search-room').on('click', function () {
        $('#date1').datetimepicker({
            format: 'L' // 'L' là định dạng ngày dài của địa phương, bạn có thể tùy chỉnh theo yêu cầu của bạn
        });
        var selectedDate = $('#date1 input').val(); // Lấy ngày được chọn
        const searchBookingRoomUrl = "{% url 'booking:search_booking_room' %}";
        $.ajax({
            type: 'POST',
            url: searchBookingRoomUrl, // Thay thế bằng URL của view Django của bạn
            data: {
                selected_date: selectedDate, // Truyền ngày được chọn trong yêu cầu POST
                csrfmiddlewaretoken: "{{ csrf_token }}", // Đảm bảo bảo mật CSRF
                action: 'post'
            },
            success: function (response) {
                console.log("Selected date:", response.selected_date);
            },
            error: function (xhr, errmsg, err) {
                console.log("Error:", errmsg);
            }
        });
    });
});

