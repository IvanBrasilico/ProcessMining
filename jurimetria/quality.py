from pm4py.algo.analysis.woflan import algorithm as woflan
from pm4py.algo.conformance.alignments import algorithm as alignments
from pm4py.algo.evaluation.replay_fitness import evaluator as replay_fitness
from pm4py.algo.evaluation.generalization import evaluator as calc_generaliz
from pm4py.algo.evaluation.precision import evaluator as calc_precision
from pm4py.algo.evaluation.simplicity import evaluator as calc_simplic
from pm4py.objects.petri.importer import importer as pnml_importer
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.algo.discovery.alpha import algorithm as alpha
import os


def cal_measure(petrinet, initial_marking, final_marking, log):
    xes_log = xes_importer.apply(os.path.join(log))
    parameters = {replay_fitness.token_replay.Parameters.ACTIVITY_KEY: 'concept:name', replay_fitness.alignment_based.Parameters.ACTIVITY_KEY: 'concept:name', woflan.Parameters.RETURN_ASAP_WHEN_NOT_SOUND: True, woflan.Parameters.PRINT_DIAGNOSTICS: False, woflan.Parameters.RETURN_DIAGNOSTICS: False, alignments.Parameters.SHOW_PROGRESS_BAR: False}
    is_sound = woflan.apply(petrinet, initial_marking, final_marking, parameters=parameters)
    if is_sound == True:
        fitness = replay_fitness.apply(xes_log, petrinet, initial_marking, final_marking, parameters=parameters, variant=replay_fitness.Variants.ALIGNMENT_BASED)
        precision = calc_precision.apply(xes_log, petrinet, initial_marking, final_marking, parameters=parameters, variant=calc_precision.Variants.ALIGN_ETCONFORMANCE)
        generaliz = calc_generaliz.apply(xes_log, petrinet, initial_marking, final_marking, parameters=parameters, variant=calc_generaliz.Variants.GENERALIZATION_TOKEN)
        simplic = calc_simplic.apply(petrinet)  # ?
        f_score = 2 * ((fitness['averageFitness'] * precision) / (fitness['averageFitness'] + precision))
        print(pn, log, 'sound', 'f_score:', f_score, 'fitness:', fitness['averageFitness'], 'precision:', precision, 'generaliz:', generaliz, 'simplic:', simplic)
    else:
        fitness = replay_fitness.apply(xes_log, petrinet, initial_marking, final_marking, parameters=parameters, variant=replay_fitness.Variants.TOKEN_BASED)
        precision = calc_precision.apply(xes_log, petrinet, initial_marking, final_marking, parameters=parameters, variant=calc_precision.Variants.ETCONFORMANCE_TOKEN)
        generaliz = calc_generaliz.apply(xes_log, petrinet, initial_marking, final_marking, parameters=parameters, variant=calc_generaliz.Variants.GENERALIZATION_TOKEN)
        simplic = calc_simplic.apply(petrinet)
        f_score = 2 * ((fitness['log_fitness'] * precision) / (fitness['log_fitness'] + precision))
        print(pn, log, 'unsound', 'f_score:', f_score, 'fitness:', fitness['log_fitness'], 'precision:', precision, 'generaliz:', generaliz, 'simplic:', simplic)

#primeiro descobrindo o modelo de processo
log = 'jurimetria/event-log.csv'

petrinet, initial_marking, final_marking = alpha.apply(log)
cal_measure(petrinet, initial_marking, final_marking, log)