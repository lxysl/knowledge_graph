class QuestionPaser:
    """构建实体节点"""

    def build_entitydict(self, args):
        entity_dict = {}
        for arg, types in args.items():
            for type in types:
                if type not in entity_dict:
                    entity_dict[type] = [arg]
                else:
                    entity_dict[type].append(arg)

        return entity_dict

    '''解析主函数'''

    def parser_main(self, res_classify):
        args = res_classify['args']
        entity_dict = self.build_entitydict(args)
        question_types = res_classify['question_types']
        sqls = []
        for question_type in question_types:
            sql_ = {'question_type': question_type}
            sql = []
            if question_type == 'disease_clinicalManifestations':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'clinicalManifestations_disease':
                sql = self.sql_transfer(question_type, entity_dict.get('clinicalManifestations'))

            elif question_type == 'disease_cause':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_relatedDiseases':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_site':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'site_disease':
                sql = self.sql_transfer(question_type, entity_dict.get('diseaseSite'))

            elif question_type == 'disease_taboo':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_drug':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'drug_disease':
                sql = self.sql_transfer(question_type, entity_dict.get('treatment'))

            elif question_type == 'disease_checks':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_diagnosis':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_prevention':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_treatment':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_doctors':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'disease_desc':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'clinicalManifestations_disease':
                sql = self.sql_transfer(question_type, entity_dict.get('clinicalManifestations'))

            if sql:
                sql_['sql'] = sql

                sqls.append(sql_)

        return sqls

    '''针对不同的问题，分开进行处理'''

    def sql_transfer(self, question_type, entities):
        if not entities:
            return []

        # 查询语句
        sql = []

        # 查询疾病有哪些症状
        if question_type == 'disease_clinicalManifestations':
            sql = ["MATCH (m:disease)-[r:r_clinicalManifestations]->(n:clinicalManifestations) where m.diseaseName =" \
                   " '{0}' return m.diseaseName, n.clinicalManifestationsName".format(i) for i in entities]

        # 查询症状会导致哪些疾病
        elif question_type == 'clinicalManifestations_disease':
            sql = ["MATCH (m:disease)-[r:r_clinicalManifestations]->(n:clinicalManifestations) where " \
                   "n.clinicalManifestationsName = '{0}' return m.diseaseName, n.clinicalManifestationsName".format(i) for i in entities]

        # 查询疾病的原因
        elif question_type == 'disease_cause':
            sql = ["match (m:disease)-[r:r_cause]->(n:cause) where m.diseaseName = '{0}' return m.diseaseName," \
                   " n.causeName".format(i) for i in entities]

        # 查询疾病的相关疾病
        elif question_type == 'disease_relatedDiseases':
            sql = ["match (m:disease)-[r:r_relatedDiseases]->(n:relatedDiseases) where m.diseaseName = '{0}' " \
                   "return m.diseaseName, n.relatedDiseasesName".format(i) for i in entities]

        # 查询疾病的发作部位
        elif question_type == 'disease_site':
            sql = ["match (m:disease)-[r:r_diseaseSite]->(n:diseaseSite) where m.diseaseName = '{0}' " \
                   "return m.diseaseName, n.diseaseSiteName".format(i) for i in entities]

        # 查询发病部位对应的疾病
        elif question_type == 'site_disease':
            sql = ["match (m:disease)-[r:r_diseaseSite]->(n:diseaseSite) where n.diseaseSiteName = '{0}' " \
                   "return m.diseaseName, n.diseaseSiteName".format(i) for i in entities]

        # 查询疾病的禁忌药物
        elif question_type == 'disease_taboo':
            sql = ["match (m:disease)-[r:r_taboos]->(n:taboos) where m.diseaseName = '{0}' " \
                   "return m.diseaseName, n.taboosName".format(i) for i in entities]

        # 查询疾病的治疗药物
        elif question_type == 'disease_drug':
            sql = ["match (m:disease)-[r:r_treatment]->(n:treatment) where m.diseaseName = '{0}' and " \
                   "r.relation_property = '药物治疗' return m.diseaseName, n.treatmentName".format(i) for i in entities]

        # 查询药物能治什么疾病
        elif question_type == 'drug_disease':
            sql = ["match (m:disease)-[r:r_treatment]->(n:treatment) where n.treatmentName = '{0}' and " \
                   "r.relation_property = '药物治疗' return m.diseaseName, n.treatmentName".format(i) for i in entities]

        # 查询疾病的检查方式
        elif question_type == 'disease_checks':
            sql = ["match (m:disease)-[r:r_checks]->(n:checks) where m.diseaseName = '{0}' " \
                   "return m.diseaseName, n.checksName".format(i) for i in entities]

        # 查询疾病的诊断方式
        elif question_type == 'disease_diagnosis':
            sql = ["match (m:disease)-[r:r_diagnosis]->(n:diagnosis) where m.diseaseName = '{0}' " \
                   "return m.diseaseName, n.diagnosisName".format(i) for i in entities]

        # 查询疾病的预防方式
        elif question_type == 'disease_prevention':
            sql = ["match (m:disease)-[r:r_prevention]->(n:prevention) where m.diseaseName = '{0}' " \
                   "return m.diseaseName, n.preventionName".format(i) for i in entities]

        # 查询疾病的治疗方式
        elif question_type == 'disease_treatment':
            sql = ["match (m:disease)-[r:r_treatment]->(n:treatment) where m.diseaseName = '{0}' " \
                   "return m.diseaseName, n.treatmentName".format(i) for i in entities]

        # 查询疾病的相关医生
        elif question_type == 'disease_doctors':
            sql = ["match (m:disease)-[r:r_relatedDoctors]->(n:relatedDoctors) where m.diseaseName = '{0}' " \
                   "return m.diseaseName, n.relatedDoctorsName".format(i) for i in entities]

        # 查询疾病的描述
        elif question_type == 'disease_desc':
            sql = ["match (m:disease) where m.diseaseName = '{0}' return m.diseaseName".format(i) for i in entities]

        # 查询疾病的临床表现
        elif question_type == 'clinicalManifestations_disease':
            sql = ["match (m:disease) where m.diseaseName = '{0}' return m.diseaseName".format(i) for i in entities]

        return sql


if __name__ == '__main__':
    handler = QuestionPaser()
