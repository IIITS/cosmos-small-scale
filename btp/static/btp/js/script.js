$(document).ready(function(){
    var hideit = ['#faculty-view', '#students-view','#submit-view', '#deadline-view'];
    for(var i=0; i<hideit.length; i++){
	$(hideit[i]).hide();	
    }	
    $('#submit-view').show();	
    $('#deadline-link').click(function(){
	for(var i=0; i<hideit.length; i++){
	$(hideit[i]).hide();
	}
	$('#deadline-view').show();
	});
    $('#faculty-link').click(function(){
    for(var i=0; i<hideit.length; i++){
	$(hideit[i]).hide();	
    }
    $('#faculty-view').show();	
    });
    $('#students-link').click(function(){
    for(var i=0; i<hideit.length; i++){
	$(hideit[i]).hide();	
    }
    $('#students-view').show();
    });
    
    $('#submissions-link').click(function(){
    
    for(var i=0; i<hideit.length; i++){
	$(hideit[i]).hide();	
    }
    $('#submissions-view').show();
    });  
    $('#submit-link').click(function(){
     for(var i=0; i<hideit.length; i++){
	$(hideit[i]).hide();	
    }
    $('#submit-view').show();	
    });      
    	    
    
});
