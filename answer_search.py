from py2neo import Graph


class AnswerSearcher:
    def __init__(self):
        self.g = Graph(
            host="127.0.0.1",
            http_port=7474,
            user="neo4j",
            password="neo4j")
        self.num_limit = 20

    '''执行cypher查询，并返回相应结果'''

    def search_main(self, sqls):
        final_answers = []
        for sql_ in sqls:
            question_type = sql_['question_type']
            queries = sql_['sql']
            answers = []
            for query in queries:
                ress = self.g.run(query).data()
                answers += ress
            final_answer = self.answer_prettify(question_type, answers)
            if final_answer:
                final_answers.append(final_answer)
        return final_answers

    '''根据对应的qustion_type，调用相应的回复模板'''

    def answer_prettify(self, question_type, answers):
        final_answer = []
        if not answers:
            return ''
        if question_type == 'disease_clinicalManifestations':
            desc = [i['n.clinicalManifestationsName'] for i in answers]
            subject = answers[0]['m.diseaseName']
            final_answer = '{0}的症状包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'clinicalManifestations_disease':
            desc = [i['m.diseaseName'] for i in answers]
            subject = answers[0]['n.clinicalManifestationsName']
            final_answer = '症状{0}可能染上的疾病有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_cause':
            desc = [i['n.causeName'] for i in answers]
            subject = answers[0]['m.diseaseName']
            final_answer = '{0}可能的成因有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_relatedDiseases':
            desc = [i['n.relatedDiseasesName'] for i in answers]
            subject = answers[0]['m.diseaseName']
            final_answer = '{0}的相关疾病包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_site':
            desc = [i['n.diseaseSiteName'] for i in answers]
            subject = answers[0]['m.diseaseName']
            final_answer = '{0}的发病部位有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'site_disease':
            desc = [i['m.diseaseName'] for i in answers]
            subject = answers[0]['n.diseaseSiteName']
            final_answer = '发病部位{0}可能的疾病有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_taboo':
            desc = [i['n.taboosName'] for i in answers]
            subject = answers[0]['m.diseaseName']
            final_answer = '{0}的禁忌药品有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_drug':
            desc = [i['n.treatmentName'] for i in answers]
            subject = answers[0]['m.diseaseName']
            final_answer = '{0}的治疗药物有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'drug_disease':
            desc = [i['m.diseaseName'] for i in answers]
            subject = answers[0]['n.treatmentName']
            final_answer = '{0}可以治疗的疾病有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_checks':
            desc = [i['n.checksName'] for i in answers]
            subject = answers[0]['m.diseaseName']
            final_answer = '{0}的检查方式有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_diagnosis':
            desc = [i['n.diagnosisName'] for i in answers]
            subject = answers[0]['m.diseaseName']
            final_answer = '{0}的诊断方式有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_prevention':
            desc = [i['n.preventionName'] for i in answers]
            subject = answers[0]['m.diseaseName']
            final_answer = '{0}的预防方式有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'disease_treatment':
            desc = [i['n.treatmentName'] for i in answers]
            subject = answers[0]['m.diseaseName']
            final_answer = '{0}的治疗方式有：{1}'.format('；'.join(list(set(desc))[:self.num_limit]), subject)

        elif question_type == 'disease_doctors':
            desc = [i['n.relatedDoctorsName'] for i in answers]
            subject = answers[0]['m.diseaseName']
            final_answer = '{0}的相关医生有：{1}'.format('；'.join(list(set(desc))[:self.num_limit]), subject)

        elif question_type == 'disease_desc':
            desc = [i['m.diseaseName'] for i in answers]
            subject = answers[0]['m.diseaseName']
            final_answer = '{0}：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'clinicalManifestations_disease':
            desc = [i['m.diseaseName'] for i in answers]
            subject = answers[0]['m.diseaseName']
            final_answer = '{0}：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        return final_answer


if __name__ == '__main__':
    searcher = AnswerSearcher()
