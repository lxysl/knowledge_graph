import os
import ahocorasick


class QuestionClassifier:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        # 特征词路径
        self.disease_path = os.path.join(cur_dir, './dict/disease.txt')
        self.department_path = os.path.join(cur_dir, './dict/department.txt')
        self.checks_path = os.path.join(cur_dir, './dict/checks.txt')
        self.cause_path = os.path.join(cur_dir, './dict/cause.txt')
        self.clinicalManifestations_path = os.path.join(cur_dir, './dict/clinicalManifestations.txt')
        self.diagnosis_path = os.path.join(cur_dir, './dict/diagnosis.txt')
        self.diseaseSite_path = os.path.join(cur_dir, './dict/diseaseSite.txt')
        self.prevention_path = os.path.join(cur_dir, './dict/prevention.txt')
        self.relatedDoctors_path = os.path.join(cur_dir, './dict/relatedDoctors.txt')
        self.taboo_path = os.path.join(cur_dir, './dict/taboos.txt')
        self.treatment_path = os.path.join(cur_dir, './dict/treatment.txt')
        self.relatedDiseases_path = os.path.join(cur_dir, './dict/relatedDiseases.txt')
        self.deny_path = os.path.join(cur_dir, './dict/deny.txt')
        # 加载特征词
        self.disease_wds = [i.strip() for i in open(self.disease_path, encoding='UTF-8') if i.strip()]
        self.department_wds = [i.strip() for i in open(self.department_path, encoding='UTF-8') if i.strip()]
        self.checks_wds = [i.strip() for i in open(self.checks_path, encoding='UTF-8') if i.strip()]
        self.cause_wds = [i.strip() for i in open(self.cause_path, encoding='UTF-8') if i.strip()]
        self.clinicalManifestations_wds = [i.strip() for i in open(self.clinicalManifestations_path, encoding='UTF-8')
                                           if i.strip()]
        self.diagnosis_wds = [i.strip() for i in open(self.diagnosis_path, encoding='UTF-8') if i.strip()]
        self.diseaseSite_wds = [i.strip() for i in open(self.diseaseSite_path, encoding='UTF-8') if i.strip()]
        self.prevention_wds = [i.strip() for i in open(self.prevention_path, encoding='UTF-8') if i.strip()]
        self.relatedDoctors_wds = [i.strip() for i in open(self.relatedDoctors_path, encoding='UTF-8') if i.strip()]
        self.taboo_wds = [i.strip() for i in open(self.taboo_path, encoding='UTF-8') if i.strip()]
        self.treatment_wds = [i.strip() for i in open(self.treatment_path, encoding='UTF-8') if i.strip()]
        self.relatedDiseases_wds = [i.strip() for i in open(self.relatedDiseases_path, encoding='UTF-8') if i.strip()]
        self.region_words = set(
            self.department_wds + self.disease_wds + self.checks_wds + self.cause_wds +
            self.clinicalManifestations_wds + self.diseaseSite_wds + self.diagnosis_wds + self.treatment_wds +
            self.prevention_wds + self.taboo_wds + self.relatedDoctors_wds + self.relatedDoctors_wds)
        self.deny_words = [i.strip() for i in open(self.deny_path, encoding='UTF-8') if i.strip()]
        # 构造领域actree
        self.region_tree = self.build_actree(list(self.region_words))
        # 构建词典
        self.wdtype_dict = self.build_wdtype_dict()
        # 问句疑问词
        self.clinicalManifestations_qwds = ['症状', '表征', '现象', '症候', '表现']
        self.causes_qwds = ['原因', '成因', '为什么', '怎么会', '怎样才', '咋样才', '怎样会', '如何会', '为啥', '为何', '如何才会', '怎么才会', '会导致',
                            '会造成', '病因']
        self.relatedDiseases_qwds = ['并发症', '并发', '一起发生', '一并发生', '一起出现', '一并出现', '一同发生', '一同出现', '伴随发生', '伴随', '共现']
        # self.food_qwds = ['饮食', '饮用', '吃', '食', '伙食', '膳食', '喝', '菜', '忌口', '补品', '保健品', '食谱', '菜谱', '食用', '食物', '补品']
        self.drug_qwds = ['药', '药品', '用药', '胶囊', '口服液', '炎片']
        self.prevention_qwds = ['预防', '防范', '抵制', '抵御', '防止', '躲避', '逃避', '避开', '免得', '逃开', '避开', '避掉', '躲开', '躲掉',
                                '绕开', '怎样才能不', '怎么才能不', '咋样才能不', '咋才能不', '如何才能不',
                                '怎样才不', '怎么才不', '咋样才不', '咋才不', '如何才不',
                                '怎样才可以不', '怎么才可以不', '咋样才可以不', '咋才可以不', '如何可以不',
                                '怎样才可不', '怎么才可不', '咋样才可不', '咋才可不', '如何可不']
        # self.lasttime_qwds = ['周期', '多久', '多长时间', '多少时间', '几天', '几年', '多少天', '多少小时', '几个小时', '多少年']
        self.treatment_qwds = ['怎么治疗', '如何医治', '怎么医治', '怎么治', '怎么医', '如何治', '医治方式', '疗法', '咋治', '怎么办', '咋办', '咋治']
        # self.cureprob_qwds = ['多大概率能治好', '多大几率能治好', '治好希望大么', '几率', '几成', '比例', '可能性', '能治', '可治', '可以治', '可以医']
        # self.easyget_qwds = ['易感人群', '容易感染', '易发人群', '什么人', '哪些人', '感染', '染上', '得上']
        self.checks_qwds = ['检查', '检查项目', '查出', '检查', '测出', '试出']
        self.department_qwds = ['属于什么科', '属于', '什么科', '科室', '科']
        self.diagnosis_qwds = ['诊断', '诊治', '诊疗']
        self.diseaseSite_qwds = ['部位', '位置', '疼', '痛', '疼痛', '不舒服', '难受']
        self.cure_qwds = ['治疗什么', '治啥', '治疗啥', '医治啥', '治愈啥', '主治啥', '主治什么', '有什么用', '有何用', '用处', '用途',
                          '有什么好处', '有什么益处', '有何益处', '用来', '用来做啥', '用来作甚', '需要', '要']
        self.taboo_qwds = ['禁忌', '忌讳', '忌口', '禁忌药物']
        self.relatedDoctors_qwds = ['名医', '医生', '医师']

        print('model init finished ......')

        return

    '''分类主函数'''

    def classify(self, question):
        data = {}
        medical_dict = self.check_medical(question)
        if not medical_dict:
            return {}
        data['args'] = medical_dict
        # 收集问句当中所涉及到的实体类型
        types = []
        for type_ in medical_dict.values():
            types += type_
        question_type = 'others'

        question_types = []

        # 症状
        # 疾病有哪些症状
        if self.check_words(self.clinicalManifestations_qwds, question) and ('disease' in types):
            question_type = 'disease_clinicalManifestations'
            question_types.append(question_type)

        # 症状会导致哪些疾病
        if self.check_words(self.clinicalManifestations_qwds, question) and ('clinicalManifestations' in types):
            question_type = 'clinicalManifestations_disease'
            question_types.append(question_type)

        # 病因
        if self.check_words(self.causes_qwds, question) and ('disease' in types):
            question_type = 'disease_cause'
            question_types.append(question_type)

        # 并发症
        if self.check_words(self.relatedDiseases_qwds, question) and ('disease' in types):
            question_type = 'disease_relatedDiseases'
            question_types.append(question_type)

        # 发病部位
        if self.check_words(self.diseaseSite_qwds, question) and ('disease' in types):
            question_type = 'disease_site'
            question_types.append(question_type)

        # 症状会导致哪些疾病
        if self.check_words(self.diseaseSite_qwds, question) and ('diseaseSite' in types):
            question_type = 'site_disease'
            question_types.append(question_type)

        # 推荐药品
        if self.check_words(self.drug_qwds, question) and 'disease' in types:
            deny_status = self.check_words(self.deny_words, question)
            if deny_status:
                question_type = 'disease_taboo'
            else:
                question_type = 'disease_drug'
            question_types.append(question_type)

        # 药品治啥病
        if self.check_words(self.treatment_qwds, question) and 'treatment' in types:
            question_type = 'drug_disease'
            question_types.append(question_type)

        # 疾病接受检查项目
        if self.check_words(self.checks_qwds, question) and 'disease' in types:
            question_type = 'disease_checks'
            question_types.append(question_type)

        # 疾病属于哪个科室
        if self.check_words(self.department_qwds, question) and 'disease' in types:
            question_type = 'disease_department'
            question_types.append(question_type)

        # 疾病接受诊断项目
        if self.check_words(self.diagnosis_qwds, question) and 'disease' in types:
            question_type = 'disease_diagnosis'
            question_types.append(question_type)

        # 症状预防
        if self.check_words(self.prevention_qwds, question) and 'disease' in types:
            question_type = 'disease_prevention'
            question_types.append(question_type)

        # 疾病治疗方式
        if self.check_words(self.treatment_qwds, question) and 'disease' in types:
            question_type = 'disease_treatment'
            question_types.append(question_type)

        # 疾病相关医生
        if self.check_words(self.relatedDoctors_qwds, question) and 'disease' in types:
            question_type = 'disease_doctors'
            question_types.append(question_type)

        # 若没有查到相关的外部查询信息，那么则将该疾病的描述信息返回
        if question_types == [] and 'disease' in types:
            question_types = ['disease_desc']

        # 若没有查到相关的外部查询信息，那么则将该疾病的描述信息返回
        if question_types == [] and 'clinicalManifestations' in types:
            question_types = ['clinicalManifestations_disease']

        # 将多个分类结果进行合并处理，组装成一个字典
        data['question_types'] = question_types

        return data

    '''构造词对应的类型'''

    def build_wdtype_dict(self):
        wd_dict = dict()
        for wd in self.region_words:
            wd_dict[wd] = []
            if wd in self.disease_wds:
                wd_dict[wd].append('disease')
            if wd in self.department_wds:
                wd_dict[wd].append('department')
            if wd in self.checks_wds:
                wd_dict[wd].append('checks')
            if wd in self.cause_wds:
                wd_dict[wd].append('cause')
            if wd in self.clinicalManifestations_wds:
                wd_dict[wd].append('clinicalManifestations')
            if wd in self.diagnosis_wds:
                wd_dict[wd].append('diagnosis')
            if wd in self.diseaseSite_wds:
                wd_dict[wd].append('diseaseSite')
            if wd in self.prevention_wds:
                wd_dict[wd].append('prevention')
            if wd in self.relatedDoctors_wds:
                wd_dict[wd].append('relatedDoctors')
            if wd in self.taboo_wds:
                wd_dict[wd].append('taboos')
            if wd in self.treatment_wds:
                wd_dict[wd].append('treatment')
            if wd in self.relatedDiseases_wds:
                wd_dict[wd].append('relatedDiseases')
        return wd_dict

    '''构造actree，加速过滤'''

    def build_actree(self, wordlist):
        actree = ahocorasick.Automaton()
        for index, word in enumerate(wordlist):
            actree.add_word(word, (index, word))
        actree.make_automaton()
        return actree

    '''问句过滤'''

    def check_medical(self, question):
        region_wds = []
        for i in self.region_tree.iter(question):
            wd = i[1][1]
            region_wds.append(wd)
        stop_wds = []
        for wd1 in region_wds:
            for wd2 in region_wds:
                if wd1 in wd2 and wd1 != wd2:
                    stop_wds.append(wd1)
        final_wds = [i for i in region_wds if i not in stop_wds]
        final_dict = {i: self.wdtype_dict.get(i) for i in final_wds}

        return final_dict

    '''基于特征词进行分类'''

    def check_words(self, wds, sent):
        for wd in wds:
            if wd in sent:
                return True
        return False


if __name__ == '__main__':
    handler = QuestionClassifier()
    while 1:
        question = input('input an question:')
        data = handler.classify(question)
        print(data)
