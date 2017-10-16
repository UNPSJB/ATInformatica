    // Inicializacion Smart Wizard
    $('#creacion_ot').smartWizard({
        labelNext:'Siguiente',
        labelPrevious:'Anterior',
        labelFinish:'Finalizar',
        onLeaveStep: function(obj, context){
            console.log("Leaving step " + context.fromStep + " to go to step " + context.toStep);
            return true;
        },
    });