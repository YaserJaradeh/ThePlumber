import json
from tqdm import tqdm
import glob
from sklearn.metrics import precision_score, recall_score, f1_score
from sklearn.preprocessing import MultiLabelBinarizer
from xml.etree.ElementTree import Element, SubElement, tostring


def convert_pipeline_output_to_webnlg_xml(pipeline: str, reference: str, output_dir: str):
    with open(pipeline, 'r') as pipeline_file, open(reference, 'r') as reference_file:
        dataset = json.load(reference_file)
        lines = pipeline_file.readlines()
        lines += ['\n'] * (len(dataset) - len(lines))
        benchmark = Element('benchmark')
        entries = SubElement(benchmark, 'entries')
        counter = 0
        pipeline_number = pipeline[pipeline.rfind('-') + 1:][:-4]
        for truth, predicted in zip(dataset, lines):
            counter += 1
            # true = truth['triples']
            pred = [{'subject': triple.split(',')[0],
                     'property': triple.split(',')[1],
                     'object': triple.split(',')[2]}
                    for triple in predicted.strip().split('\t')
                    if len(triple) > 0]
            entry = SubElement(entries, 'entry', {'category': truth['category'], 'eid': f'Id{counter}'})
            generated_triple_set = SubElement(entry, 'generatedtripleset')
            for triple in pred:
                gtriple = SubElement(generated_triple_set, 'gtriple')
                gtriple.text = f"{triple['subject']} | {triple['property']} | {triple['object']}"
        with open(f'{output_dir}/result-{pipeline_number}.xml', 'w') as out_file:
            out_file.write(tostring(benchmark, 'unicode'))
            out_file.flush()
        convert_ref_output_to_webnlg_xml(reference)


def convert_all_pipelines_to_webnlg_xml(directory: str, reference: str, output_dir: str):
    files = glob.glob(f"{directory}{'/' if directory[-1] != '/' else ''}*.tsv")
    for file in files:
        convert_pipeline_output_to_webnlg_xml(file, reference, output_dir)


def convert_ref_output_to_webnlg_xml(reference: str):
    with open(reference, 'r') as reference_file:
        dataset = json.load(reference_file)
        benchmark = Element('benchmark')
        entries = SubElement(benchmark, 'entries')
        counter = 0
        for truth in dataset:
            counter += 1
            true = truth['triples']
            entry = SubElement(entries, 'entry', {'category': truth['category'], 'eid': f'Id{counter}'})
            modified_triple_set = SubElement(entry, 'modifiedtripleset')
            for triple in true:
                mtriple = SubElement(modified_triple_set, 'mtriple')
                mtriple.text = f"{triple['subject'].strip()} | {triple['property'].strip()} | {triple['object'].strip()}"
        with open('reference.xml', 'w') as out_file:
            out_file.write(tostring(benchmark, 'unicode'))
            out_file.flush()


def compute_metrics_per_pipeline(directory: str, reference: str):
    files = glob.glob(f"{directory}{'/' if directory[-1] != '/' else ''}*.tsv")
    for file in tqdm(files):
        with open(file, 'r') as pipeline_file, open(reference, 'r') as reference_file:
            # Prepare data
            dataset = json.load(reference_file)
            lines = pipeline_file.readlines()
            lines += ['\n'] * (len(dataset) - len(lines))
            # Get pipeline number
            pipeline_number = file[file.rfind('-') + 1:][:-4]
            print('-----------------------------------------------------------------')
            print(f'Pipeline {pipeline_number}:')
            print('-----------------------------------------------------------------')
            # Start counting metrics
            truth_triples = []
            predicted_triples = []
            for truth, predicted in zip(dataset, lines):
                # Collect triples
                truth_triples.append(truth['triples'])
                predicted_triples.append([{'subject': triple.split(',')[0],
                                           'property': triple.split(',')[1],
                                           'object': triple.split(',')[2]}
                                          if len(triple) > 0
                                          else {'subject': '',
                                                'property': '',
                                                'object': ''}
                                          for triple in predicted.strip().split('\t')])
            # Collect individual components to compute metrics
            # =================== Subjects ===================
            true_subjects = [[triple['subject'] for triple in triples] for triples in truth_triples]
            pred_subjects = [[triple['subject'] for triple in triples] for triples in predicted_triples]
            true_subjects, pred_subjects = binarize_classes(pred_subjects, true_subjects)
            subj_p = precision_score(true_subjects, pred_subjects, average='weighted', zero_division=0)
            subj_r = recall_score(true_subjects, pred_subjects, average='weighted', zero_division=0)
            subj_f1 = f1_score(true_subjects, pred_subjects, average='weighted', zero_division=0)
            # =================== Predicates ===================
            true_predicates = [[triple['property'] for triple in triples] for triples in truth_triples]
            pred_predicates = [[triple['property'] for triple in triples] for triples in predicted_triples]
            true_predicates, pred_predicates = binarize_classes(pred_predicates, true_predicates)
            pred_p = precision_score(true_predicates, pred_predicates, average='weighted', zero_division=0)
            pred_r = recall_score(true_predicates, pred_predicates, average='weighted', zero_division=0)
            pred_f1 = f1_score(true_predicates, pred_predicates, average='weighted', zero_division=0)
            # =================== Objects ===================
            true_objects = [[triple['object'] for triple in triples] for triples in truth_triples]
            pred_objects = [[triple['object'] for triple in triples] for triples in predicted_triples]
            true_objects, pred_objects = binarize_classes(pred_objects, true_objects)
            obj_p = precision_score(true_objects, pred_objects, average='weighted', zero_division=0)
            obj_r = recall_score(true_objects, pred_objects, average='weighted', zero_division=0)
            obj_f1 = f1_score(true_objects, pred_objects, average='weighted', zero_division=0)
            print('-----------------------------------------------------------------')
            print('Partial scores')
            print('-----------------------------------------------------------------')
            print('Subjects:')
            print(f'Precision: {subj_p}')
            print(f'Recall: {subj_r}')
            print(f'F1-Score: {subj_f1}')
            print('------------------------------------')
            print('Predicates:')
            print(f'Precision: {pred_p}')
            print(f'Recall: {pred_r}')
            print(f'F1-Score: {pred_f1}')
            print('------------------------------------')
            print('Objects:')
            print(f'Precision: {obj_p}')
            print(f'Recall: {obj_r}')
            print(f'F1-Score: {obj_f1}')
            # return


def binarize_classes(pred, true):
    newreflist = [[string.lower() for string in sublist] for sublist in true]
    newcandlist = [[string.lower() for string in sublist] for sublist in pred]
    # First get all the classes by combining the triples in the candidatelist and referencelist
    allclasses = newcandlist + newreflist
    allclasses = [item for items in allclasses for item in items]
    allclasses = list(set(allclasses))
    lb = MultiLabelBinarizer(classes=allclasses)
    mcbin = lb.fit_transform(newcandlist)
    mrbin = lb.fit_transform(newreflist)
    return mrbin, mcbin


if __name__ == '__main__':
    convert_all_pipelines_to_webnlg_xml(
        '../results/dbp/plumber/WebNLG-2017-train/',
        '../datasets/WebNLG/webnlg_v2_train.json',
        './xml'
    )
    # convert_pipeline_output_to_webnlg_xml(
    #     '../results/dbp/plumber/WebNLG-2017-dev/pipeline-0.tsv',
    #     '../datasets/WebNLG/webnlg_v2_dev.json',
    #     './xml'
    # )
    # compute_metrics_per_pipeline(
    #     '../results/dbp/plumber/WebNLG-2017-dev',
    #     '../datasets/WebNLG/webnlg_v2_dev.json'
    # )
