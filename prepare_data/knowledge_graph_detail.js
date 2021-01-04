$(function () {
    demo();
    jiexi($("#name").val(), $("#name").val());
    searchRelated(0, "literature");
    searchRelatedOrg();
    searchRelatedGraph();
})

function demo() {
    $.ajax({
        type: "post",
        url: "./getknowgraphDetail.do",
        data: {
            title: $("#name").val()
        },
        dataType: "json",
        async: false,
        success: function (res) {
            $("#id").val(res[0]['id']);
            $("#category").val(res[0]['category']);
            //初始化知识图谱下的内容
            var know_detail = '';
            //疾病知识图谱详情页
            for (var i = 0; i < 5; i++) {
                if (res[0]['species'] == "disease") {
                    switch (i) {
                        case 0:
                            property = 'abstracts';//概述
                            propertyZH = '概述';
                            break;
                        case 1:
                            property = 'symptoms';//症状
                            propertyZH = '症状';
                            break;
                        case 2:
                            property = 'diagnosis';//诊断
                            propertyZH = '诊断';
                            break;
                        case 3:
                            property = 'treatment';//治疗
                            propertyZH = '治疗';
                            break;
                        default:
                            property = 'checks';//检查
                            propertyZH = '检查';
                            break;
                    }
                    if (!empty(res[0][property])) {
                        var atype = i < 2 ? 1 : 0;
                        know_detail += '<dl>';
                        know_detail += '<dt><a type="' + atype + '" href="javascript:void(0)">' + propertyZH + '<span class="wiki_icon"></span></a></dt>';
                        know_detail += '<dd style="height: auto; display: -webkit-box; overflow: hidden;">' + res[0][property] + '</dd>';
                        know_detail += '<dd><a href="javascript:void(0)" type="0">展开</a></dd>';
                        know_detail += '</dl>';
                    }
                }
            }
            //药物知识图谱详情页
            for (var i = 0; i < 6; i++) {
                if (res[0]['species'] == "medicine") {
                    switch (i) {
                        case 0:
                            property = 'drug_aliases'; //药物别名
                            propertyZH = '别名';
                            break;
                        case 1:
                            property = 'drug_properties'; //药物属性
                            propertyZH = '性状';
                            break;
                        case 2:
                            property = 'drug_indications'; //合理用药
                            propertyZH = '适应症';
                            break;
                        case 3:
                            property = 'adverse_drug_reactions'; //药物不良反应
                            propertyZH = '不良反应';
                            break;
                        case 4:
                            property = 'matters_needing_attention'; //注意事项
                            propertyZH = '注意事项';
                            break;
                        case 5:
                            property = 'contraindication'; //禁忌症
                            propertyZH = '禁忌症';
                            break;
                        default:
                            property = 'checks';//检查
                            propertyZH = '检查';
                            break;
                    }
                    if (!empty(res[0][property])) {
                        var atype = i < 2 ? 1 : 0;
                        know_detail += '<dl>';
                        know_detail += '<dt><a type="' + atype + '" href="javascript:void(0)">' + propertyZH + '<span class="wiki_icon"></span></a></dt>';
                        know_detail += '<dd style="height: auto; display: -webkit-box; overflow: hidden;word-break:break-all;">' + res[0][property] + '</dd>';
                        know_detail += '<dd><a href="javascript:void(0)" type="0">展开</a></dd>';
                        know_detail += '</dl>';
                    }
                }
            }
            $("#know_detail").html(know_detail);
            //详细字段内容切换
            $(".know_detail dt a").click(function () {
                var emtype = $(this).attr("type");
                if (emtype == "1") {
                    $(this).parents("dl").css({
                        "height": "40px"
                    });
                    $(this).attr("type", "0");
                } else if (emtype == "0") {
                    $(this).parents("dl").css({
                        "height": "auto"
                    });
                    $(this).attr("type", "1");
                }
            });
            //详细字段内容展开收起
            $(".know_detail dd a").click(function () {
                var emtype = $(this).attr("type");
                if (emtype == "1") {
                    $(this).parents("dl").find("dd").eq(0).css({
                        "height": "300px",
                        "display": "-webkit-box",
                        "overflow": "hidden"
                    });
                    $(this).text("展开");
                    $(this).css(
                        "background-image",
                        "url(mkb/static/img/icon_zhan.png)"
                    );
                    $(this).attr("type", "0")
                } else if (emtype == "0") {
                    $(this).parents("dl").find("dd").eq(0).css({
                        "height": "auto",
                        "display": "block",
                        "overflow": "inherit"
                    });
                    $(this).text("收起");
                    $(this).css(
                        "background-image",
                        "url(mkb/static/img/icon_shou.png)"
                    );
                    $(this).attr("type", "1")
                }
            });
            $('.know_tab_con dl dd:first-of-type:visible').each(function (i, val) {
                if ($('.know_tab_con dl dd:first-of-type:visible')[i].scrollHeight <= 300) {
                    $(this).next().hide();
                } else {
                    $(this).css({
                        "height": "300px",
                        "display": "-webkit-box",
                        "overflow": "hidden"
                    });
                }
            });
        },
        error: function (jqXHR, textStatus, errorThrown) {
        }
    });
}

function jiexi(id, name) {
    $.ajax({
        type: "post",
        url: "./knowledgeGraphs.do",
        data: {name: name},
        dataType: "json",
        async: false,
        success: function (data) {
            var linksArray = new Array();
            var nodesArray = new Array();
            if (!empty(data)) {
                $(data).each(function (i) {
                    if (!empty(data[i])) {
                        var name = data[i].name;
                        var id = data[i].id;
                        var target = data[i].target;
                        var category = data[i].category;
                        var value = data[i].value;
                        var weight = 5;

                        if (category == '1') {
                            nodesArray.push({
                                category: category,
                                name: name,
                                value: value,
                                url: getId(name),
                            });
                        } else {
                            nodesArray.push({
                                category: category,
                                name: name,
                                value: value,
                            });
                        }

                        if ("1" == category + '') {
                            weight = 2;
                        } else if ("2" == category + '') {
                            weight = 0.8;
                        } else if ("3" == category + '') {
                            weight = 1;
                        } else if ("4" == category + '') {
                            weight = 1;
                        }
                        linksArray.push({
                            "source": id,
                            "target": target,
                            "weight": weight
                        });
                    }
                });
                var categoriesArray = new Array();
                categoriesArray.push({
                    name: '名称',
                    itemStyle: {
                        normal: {
                            color: '#EE7600'
                        }
                    }
                });
                categoriesArray.push({
                    name: '名称',
                    itemStyle: {
                        normal: {
                            color: '#FFAEB9'
                        }
                    }
                });
                categoriesArray.push({
                    name: '名称',
                    itemStyle: {
                        normal: {
                            color: '#FFA54F'
                        }
                    }
                });
                categoriesArray.push({
                    name: '名称',
                    itemStyle: {
                        normal: {
                            color: '#4F94CD'
                        }
                    }
                });
            }
            // 基于准备好的dom，初始化echarts实例
            var myChart = echarts.init(document.getElementById("echart_box"));
            // 指定图表的配置项和数据
            option = {
                title: {
                    x: 'right',
                    y: 'bottom'
                },
                tooltip: {
                    trigger: 'item',
                    formatter: '{a} : {b}'
                },
                toolbox: {
                    show: true,
                    feature: {
                        restore: {
                            show: true
                        },
                        magicType: {
                            show: true,
                            type: ['force', 'chord']
                        },
                        saveAsImage: {
                            show: true
                        }
                    }
                },
                legend: {
                    x: 'left',
                    data: ['']
                },
                series: [{
                    type: 'force',
                    name: "名称",
                    ribbonType: false,
                    categories: categoriesArray,
                    itemStyle: {
                        normal: {
                            label: {
                                show: true,
                                textStyle: {
                                    color: '#444'
                                }
                            },
                            nodeStyle: {
                                brushType: 'both',
                                borderColor: 'rgba(255,215,0,0.4)',
                                borderWidth: 0
                            },
                            linkStyle: {
                                type: 'curve'
                            }
                        },
                        emphasis: {
                            label: {
                                show: false
                            },
                            nodeStyle: {},
                            linkStyle: {}
                        }
                    },
                    useWorker: false,
                    minRadius: 15,
                    maxRadius: 25,
                    gravity: 1.1,
                    scaling: 1.1,
                    roam: 'move',
                    nodes: nodesArray,
                    links: linksArray,

                }]
            };
            var ecConfig = echarts.config;

            function focus(param) {
                var data = param.data;
                var links = option.series[0].links;
                var nodes = option.series[0].nodes;
                if (
                    data.source !== undefined
                    && data.target !== undefined
                ) { //点击的是边
                    var sourceNode = nodes.filter(function (n) {
                        return n.name == data.source
                    })[0];
                    var targetNode = nodes.filter(function (n) {
                        return n.name == data.target
                    })[0];
                } else { // 点击的是点
                }
            }

            myChart.on(ecConfig.EVENT.CLICK, focus)
            myChart.on(ecConfig.EVENT.FORCE_LAYOUT_END, function () {
            });
            myChart.setOption(option);
            $('.know_echart').resize(function () {
                myChart.resize();
            });
            $("#echart_box").show();
            var img = 'mkb/static/img/knowledge/' + $("#id").val() + '.png';
            if (!fileExists(img)) {
                setTimeout(function () {
                    saveAsImg(myChart);
                }, 3000);
            }
        }
    });
}

function saveAsImg(myChart) {
    var picBase64Info = myChart.getDataURL();
    $.ajax({
        type: "post",
        url: "./saveEchartImg.do",
        data: {
            name: $("#id").val(),
            base64Info: picBase64Info
        },
        dataType: "json",
        async: false,
        success: function (data) {

        },
        error: function () {

        }
    });
}

function getId(name) {
    var map = new Map();
    map.put('危险因素', 'riskFactors');
    map.put('临床表现', 'clinicalManifestations');
    map.put('预防', 'prevention');
    map.put('', 'treatmentGuidelines');
    map.put('', 'complicationsTreatment');
    map.put('', 'strokeCareUnitAndStrokeUnit');
    map.put('', 'acuteCerebralInfarctionTreatment');
    map.put('', 'drugTreatment');
    map.put('', 'relatedDiseases');
    map.put('病因', 'cause');
    map.put('症状', 'symptoms');
    map.put('诊断', 'diagnosis');
    map.put('治疗', 'treatment');
    map.put('检查', 'checks');
    var id = map.get(name);
    if (null == id) {
        id = '';
    }
    return id;
}

//检索相关资源
function searchRelated(id, searchType, searchFields) {
    $.ajax({
        type: "post",
        data: {
            "id": id,
            "keywords": $("#name").val(),
            "searchType": searchType,
            "searchFields": searchFields
        },
        url: "searchRelated.do",
        dataType: "json",
        traditional: true,
        beforeSend: function (XMLHttpRequest) {
        },
        success: function (data) {
            if (!empty(data) && data.length > 0) {
                var content = '<ul>';
                for (var i in data) {
                    var id = data[i]['id'];
                    var title = data[i]['title'];
                    var href = 'details.html?id=' + id + '&classesEn=' + searchType;
                    content += '<li><a href="' + href + '" title="' + title + '">' + title + '</a></li>';
                }
                content += '</ul>';

                $('#related_' + searchType).show();
                $('#related_' + searchType + ' .related_list').html(content);
            } else {
                $('#related_' + searchType).hide();
            }
        },
        error: function () {
        }
    });
}

//相关图谱
function searchRelatedGraph() {
    $.ajax({
        type: "post",
        data: {
            "id": $("#id").val(),
            "keywords": $("#name").val()
        },
        url: "searchRelatedGraph.do",
        dataType: "json",
        traditional: true,
        beforeSend: function (XMLHttpRequest) {
        },
        success: function (data) {
            if (!empty(data) && data.length > 0) {
                var content = '<ul class="clearfix">';
                for (var i in data) {
                    var id = data[i]['id'];
                    var title = data[i]['title'];
                    content += '<li><a href="toKnowgraphDetail.html?title=' + title;
                    content += '" target="_blank"><img src="mkb/static/img/knowledge/' + id + '.png"><p>' + title + '</p></a></li>';
                }
                content += '</ul>';

                $('#related_graph').show();
                $('#related_graph .related_list').html(content);
            } else {
                $('#related_graph').hide();
            }
        },
        error: function () {
        }
    });
}

//相关机构
function searchRelatedOrg() {
    var searchType = "organization";
    $.ajax({
        type: "post",
        data: {
            "id": $("#id").val(),
            "keywords": $("#name").val(),
            "category": $("#category").val()
        },
        url: "searchRelatedOrg.do",
        dataType: "json",
        traditional: true,
        beforeSend: function (XMLHttpRequest) {
        },
        success: function (data) {
            if (!empty(data) && data.length > 0) {
                var content = '<ul>';
                for (var i in data) {
                    var id = data[i]['id'];
                    var title = data[i]['title'];
                    var href = 'details.html?id=' + id + '&classesEn=' + searchType;
                    content += '<li><a href="' + href + '" title="' + title + '">' + title + '</a></li>';
                }
                content += '</ul>';
                $('#related_' + searchType).show();
                $('#related_' + searchType + ' .related_list').html(content);
            } else {
                $('#related_' + searchType).hide();
            }
        },
        error: function () {
        }
    });
}

//---------------- 通用方法 ------------------//
//判断文件是否存在
function fileExists(url) {
    var isExists;
    $.ajax({
        url: url,
        async: false,
        type: 'HEAD',
        error: function () {
            isExists = false;
        },
        success: function () {
            isExists = true;
        }
    });
    return isExists;
}

// 判断是否非空
function empty(v) {
    switch (typeof v) {
        case 'undefined' :
            return true;
        case 'string' :
            if (trim(v).length == 0)
                return true;
            break;
        case 'boolean' :
            if (!v)
                return true;
            break;
        case 'number' :
            if (0 === v)
                return true;
            break;
        case 'object' :
            if (null === v)
                return true;
            if (undefined !== v.length && v.length == 0)
                return true;
            if (v == '') {
                return true;
            }
            for (var k in v) {
                return false;
            }
            return true;
            break;
    }
    return false;
}

//去左空格;
function ltrim(s) {
    return s.replace(/^(\s*|　*)/, "");
}

//去右空格;
function rtrim(s) {
    return s.replace(/(\s*|　*)$/, "");
}

//去左右空格;
function trim(s) {
    return ltrim(rtrim(s));
}