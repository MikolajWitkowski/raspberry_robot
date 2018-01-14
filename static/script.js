$(document).ready(function(){

	var keyPress = false;
	var run = false;
    var camera = false;
    var distance = false;
    var distance_pause = false;
	 
     
    function update_speed(){
		
		$.getJSON('get_data', {}, function(data){        
                $('.speed').html(data.speed +' %');
                });
    }
    
     function update_dist(){
		
		$.getJSON('get_data', {}, function(data){        
               $('.distance').html(data.distance +' cm');
                });
    }

	$('.run').click(function(){
        $(this).toggleClass('stop');
        $(this).html($(this).html() == 'run' ? 'stop':'run');
		if (run == false){			
            int_speed = setInterval(update_speed, 1000);
            run = true;
           
        }else{
            clearInterval(int_speed);
            run = false;
            }
    });
    
    
    $('.rec').click(function(){
        $(this).html($(this).html() == 'off' ? 'on':'off')
        $(this).toggleClass('on');
        if (camera == false){
            $.get('/play_video');
        
            setTimeout(function(){
              //  $('.video_img').attr('src', 'http://192.168.1.10:8080/stream/video.mjpeg')		
				$('.video_img').attr('src', 'http://192.168.43.170:8080/stream/video.mjpeg')
            }, 3000);
            camera = true;
            
        }else{
            $.get('/stop_video');
            $('.video_img').attr('src', '');
            camera = false;
            }
        });
    
    $('.dist').click(function(){
		$(this).html('on');
		$(this).addClass('on');
             
        if (distance == false){
			 
            int_dist = setInterval(update_dist, 1000);
            distance = true;
            $.get('/start_distance');
          
			}
		}); 
		
	$('.dist_pause').click(function(){
		$(this).html($(this).html() == 'pause' ? 'resume':'pause')
		if (distance_pause == false){
			$.get('/pause_distance');
			distance_pause = true;
			clearInterval(int_dist);
			$('.distance').html('pause')
					
		}else{
			$.get('/resume_distance');
			distance_pause = false;
			int_dist = setInterval(update_dist, 1000);
			}
		
		})


	var down = {87: false, 83: false, 65: false, 68: false, 75: false, 
		76: false, 90:false, 88: false, 77:false, 188:false, 190:false};
	$(document).keydown(function(e){
		if (e.keyCode in down && run == true){
			down[e.keyCode] = true;
			if(down[87]){
				$.get('/forward');
				}
			if(down[83]){
				$.get('/backward')
				}
			if(down[65]){
				$.get('/left')
				}
			if (down[68]){
				$.get('/right')
				}		
			if(down[75]){
				$.get('/speed_down');
				}
			if(down[76]){
				$.get('/speed_up');
				}
                
            if(down[77]){
                $.get('/start_distance');
                }
            if(down[188]){
                $.get('/pause_distance');
                }
            if(down[190]){
                $.get('/stop_distance');
                }
                }
		}).keyup(function(e){
			if (e.keyCode in down){
				down[e.keyCode] = false;
				if (e.keyCode == 87 || e.keyCode == 83 || e.keyCode == 65 || e.keyCode == 68){	
					$.get('/stop')
				}
                if(e.keyCode == 88){
                    $.get('/move_camera_left');
                    $('.cam_poz').animate({'marginLeft': "+=5px"}, 50);
                    
                    }   
                if(e.keyCode == 90){
                    $.get('/move_camera_right');
                    $('.cam_poz').animate({'marginLeft': "-=5px"}, 50);
                    
                    }
            }
        });
});
