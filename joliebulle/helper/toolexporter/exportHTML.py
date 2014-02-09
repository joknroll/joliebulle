#!/usr/bin/python3
#­*­coding: utf­8 -­*­

#joliebulle 3.1
#Copyright (C) 2010-2013 Pierre Tavares
#Copyright (C) 2013 Thomas Gerbet

#This program is free software; you can redistribute it and/or
#modify it under the terms of the GNU General Public License
#as published by the Free Software Foundation; either version 3
#of the License, or (at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.


from PyQt4.QtCore import QCoreApplication




def exportHTML():
    resultHtml = '''
<!doctype html>
<html>
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<script src="angular/angular.min.js"></script>
<script src="jquery/jquery.js"></script>
<script src="bootstrap/js/bootstrap.min.js"></script>
<script src="controllers/tools/main.js"></script>
<script src="controllers/tools/gravity.js"></script>
<script src="controllers/tools/steps.js"></script>
<script src="controllers/tools/alcool.js"></script>
<script src="controllers/tools/dilution.js"></script>
<script src="controllers/tools/boiloff.js"></script>
<script src="controllers/tools/decoction.js"></script>
<script src="controllers/tools/sgplato.js"></script>
<link rel="stylesheet" href="bootstrap/css/bootstrap.min.css">
<link rel="stylesheet" href="font-awesome/css/font-awesome.min.css">


<style>
    body {background:url(images/furley_bg.png);}
    .menu{text-align: right; color: #999; font-size: 24px;float:right;margin: auto; padding-top:0.6em;}
    .menu i:hover{color:#333333;}
    .menu ul{text-align: left;}
    .tools-header {padding-bottom:1em;margin: auto;float:left;}
    .tools-header h1 {color:#999;font-weight:bold; font-size:24px ;}
    .tool-block {margin-top:3em; margin-bottom:1em; background-color: white; border: 1px solid rgba(0, 0, 0, 0.1);box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.08);padding: 50px;padding-top: 0;}
    h3{margin-bottom: 2em;}
    .tool-result{margin-top:4em;}
    .last{margin-bottom: 3em;}
    .row-tools{padding-left: 15px; padding-right: 15px;}
.tool-result{margin-top:4em;}


input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
    /* display: none; <- Crashes Chrome on hover */
    -webkit-appearance: none;
    margin: 0; /* <-- Apparently some margin are still there even though it's hidden */
}

</style>

</head>
'''    
    

    resultHtml +=''' <body ng-app="tools">

    <div class="container">

        <div class="row">
            <div class="tools-header col-sm-3">
                <h1>{0}</h1>
            </div>
            <div class="menu btn-group col-sm-2 col-sm-offset-7">
                <i class="icon-reorder" data-toggle="dropdown"></i>
                <ul class="dropdown-menu pull-right" role="menu">    
                                <li><a href="#gravity">{1}</a></li>
                                <li><a href="#step">{2}</a></li>
                                <li><a href="#alc">{3}</a></li>
                                <li><a href="#dilution">{4}</a></li>
                                <li><a href="#boiloff">{5}</a></li>
                                <li><a href="#decoc">{6}</a></li>
                                <li><a href="#sg">{7}</a></li>
                              </ul>
                        
            </div>
        </div>''' .format(QCoreApplication.translate("Export","Outils", None, QCoreApplication.UnicodeUTF8), QCoreApplication.translate("Export","Correction du densimètre", None, QCoreApplication.UnicodeUTF8), QCoreApplication.translate("Export","Assistant paliers", None, QCoreApplication.UnicodeUTF8), QCoreApplication.translate("Export","Taux d'alcool", None, QCoreApplication.UnicodeUTF8), QCoreApplication.translate("Export","Dilution", None, QCoreApplication.UnicodeUTF8), QCoreApplication.translate("Export","Evaporation", None, QCoreApplication.UnicodeUTF8), QCoreApplication.translate("Export","Décoction", None, QCoreApplication.UnicodeUTF8), QCoreApplication.translate("Export","Densité - Plato", None, QCoreApplication.UnicodeUTF8))



    resultHtml+='''<div class="row row-tools" id="gravity">
            <div ng-controller="GravityToolCtrl" class="tool-block">
                <h3>{0}</h3>
                <form class="form-horizontal" role="form">
                <div class="form-group">
                    <label class="col-sm-3 control-label">{1}</label>
                    <div class="col-sm-2">
                        <input type="number" min="1.000" max="1.999" step="0.001" ng-model="measuredGravity" class="form-control">
                    </div>
                </div>
                <div class="form-group">
                    <label class="col-sm-3 control-label">{2}</label>
                    <div class="col-sm-2">
                        <input type="number" min="0" max="100" step="1" ng-model="calibTemp" class="form-control">
                    </div>
                </div>
                <div class="form-group">
                    <label class="col-sm-3 control-label">{3}</label>
                    <div class="col-sm-2">
                        <input type="number" min="0" max="110" step="1" ng-model="sampleTemp" class="form-control">
                    </div>
                </div>
                <div class="form-group tool-result">
                    <label class="col-sm-3 control-label">{4}</label>
                    <div class="col-sm-2">
                        <label class="control-label">{5}</label>
                    </div>
                </div>
                </form>
            </div>
        </div>''' .format(QCoreApplication.translate("Export","Correction du densimètre", None, QCoreApplication.UnicodeUTF8),QCoreApplication.translate("Export","Densité mesurée", None, QCoreApplication.UnicodeUTF8),QCoreApplication.translate("Export","Température de calibration (°C)", None, QCoreApplication.UnicodeUTF8), QCoreApplication.translate("Export","Température mesurée (°C)", None, QCoreApplication.UnicodeUTF8),QCoreApplication.translate("Export","Densité corrigée", None, QCoreApplication.UnicodeUTF8), "{{calcGravity()}}")


    resultHtml+='''<div class="row row-tools" id="step">
            <div ng-controller="StepAssistantCtrl" class="tool-block">
                <h3>{0}</h3>
                <form class="form-horizontal" role="form">
                    <div class="form-group">
                        <label class="col-sm-3 control-label">Mode</label>
                        <div class="col-sm-3">
                            <select ng-model="stepType" ng-options="type for type in stepTypes " class="form-control"></select>
                        </div>
                    </div>
                    <div class="form-group">
                        <label class="col-sm-3 control-label">{1}</label>
                        <div class="col-sm-3">
                            <input type="number" min="1.000" max="100" step="1" ng-model="targetTemp" class="form-control">
                        </div>
                    </div>
                    <div class="form-group">
                        <label class="col-sm-3 control-label">{2}</label>
                        <div class="col-sm-3">
                            <input type="number" min="0" max="10000" step="1" ng-model="addedVolume" class="form-control">
                        </div>
                    </div>
                    <div class="form-group">
                        <label class="col-sm-3 control-label">{3}</label>
                        <div class="col-sm-3">
                            <input type="number" min="0" max="10000" step="1" ng-model="grainWeight" class="form-control">
                        </div>
                    </div>
                    <div class="form-group" ng-hide="stepType=='Palier'">
                        <label class="col-sm-3 control-label">{4}</label>
                        <div class="col-sm-3">
                            <input type="number" min="0.1" max="100" step="1" ng-model="grainTemp" class="form-control">
                        </div>
                    </div>
                    <div class="form-group" ng-hide="stepType=='Empâtage'">
                        <label class="col-sm-3 control-label">{5}</label>
                        <div class="col-sm-3">
                            <input type="number" min="0.1" max="100" step="1" ng-model="mashTemp" class="form-control">
                        </div>
                    </div>
                    <div class="form-group" ng-hide="stepType=='Empâtage'">
                        <label class="col-sm-3 control-label">{6}</label>
                        <div class="col-sm-3">
                            <input type="number" min="0" max="10000" step="1" ng-model="waterVolumeMash" class="form-control">
                        </div>
                    </div>
                    <div class="form-group">
                        <label class="col-sm-3 control-label">{7}</label>
                        <div class="col-sm-3">
                            <input type="number" min="0" max="100" step="1" ng-model="factor" class="form-control">
                        </div>
                    </div>
                    <div class="form-group tool-result">
                    <label class="col-sm-3 control-label">{8}</label>
                    <div class="col-sm-3">
                        <label class="control-label">{9}</label>
                    </div>
                    </div>
                    <div class="form-group">
                    <label class="col-sm-3 control-label">{10}</label>
                    <div class="col-sm-3">
                        <label class="control-label">{11}</label>
                    </div>
                    </div>
                </form>
            </div>
        </div>''' .format(QCoreApplication.translate("Export","Assistant paliers", None, QCoreApplication.UnicodeUTF8), QCoreApplication.translate("Export","Température cible (°C)", None, QCoreApplication.UnicodeUTF8), QCoreApplication.translate("Export","Volume ajouté (L)", None, QCoreApplication.UnicodeUTF8), QCoreApplication.translate("Export","Poids du grain (Kg)", None, QCoreApplication.UnicodeUTF8),QCoreApplication.translate("Export","Température du grain (°C)", None, QCoreApplication.UnicodeUTF8),QCoreApplication.translate("Export","Température de la maîche (°C)", None, QCoreApplication.UnicodeUTF8),QCoreApplication.translate("Export","Volume d'eau dans la maîche (L)", None, QCoreApplication.UnicodeUTF8),QCoreApplication.translate("Export","Facteur de correction", None, QCoreApplication.UnicodeUTF8),QCoreApplication.translate("Export","Température de l'eau (°C)", None, QCoreApplication.UnicodeUTF8),"{{waterTemp().temp}}",QCoreApplication.translate("Export","Ratio (L/Kg)", None, QCoreApplication.UnicodeUTF8),"{{waterTemp().ratio}}")



    resultHtml+='''<div class="row row-tools" id="alc">
            <div ng-controller="AlcToolCtrl" class="tool-block">
                <h3>{0}</h3>
                <form class="form-horizontal" role="form">
                <div class="form-group">
                    <label class="col-sm-3 control-label">{1}</label>
                    <div class="col-sm-2">
                        <input type="number" class="form-control" min="0.001" max="100" step="0.001" ng-model="originalGravity">
                    </div>
                </div>
                <div class="form-group">
                    <label class="col-sm-3 control-label">{2}</label>
                    <div class="col-sm-2">
                        <input type="number" class="form-control" min="0.001" max="100" step="0.001" ng-model="finalGravity">
                    </div>
                </div>
                <div class="form-group">
                    <label class="col-sm-3 control-label">{3}</label>
                    <div class="col-sm-2">
                        <input type="number" class="form-control" min="0" max="100000" step="1" ng-model="addedSugar">
                    </div>
                </div>
                <div class="form-group tool-result">
                    <label class="col-sm-3 control-label">{4}</label>
                    <div class="col-sm-2">
                        <label class="control-label">{5}</label>
                    </div>
                </div>
                </form>
            </div>
        </div>'''.format(QCoreApplication.translate("Export","Taux d'alcool", None, QCoreApplication.UnicodeUTF8),QCoreApplication.translate("Export","Densité initiale", None, QCoreApplication.UnicodeUTF8),QCoreApplication.translate("Export","Densité finale", None, QCoreApplication.UnicodeUTF8), QCoreApplication.translate("Export","Sucre ajouté (g/L)", None, QCoreApplication.UnicodeUTF8),QCoreApplication.translate("Export","Alcool par volume (%)", None, QCoreApplication.UnicodeUTF8),"{{calcAlcoolVol()}}")



    resultHtml+='''<div class="row row-tools" id="dilution">
            <div ng-controller="DilutionToolCtrl" class="tool-block">
                <h3>{0}</h3>
                <form class="form-horizontal" role="form">
                <div class="form-group">
                    <label class="col-sm-3 control-label">{1}</label>
                    <div class="col-sm-2">
                        <input type="number" class="form-control" min="0" max="10000000" step="1" ng-model="initialVol">
                    </div>
                </div>
                <div class="form-group">
                    <label class="col-sm-3 control-label" >{2}</label>
                    <div class="col-sm-2">
                        <input type="number"  class="form-control" min="0.001" max="100" step="0.001" ng-model="initialGravity">
                    </div>
                </div>
                <div class="form-group">
                    <label class="col-sm-3 control-label">{3}</label>
                    <div class="col-sm-2">
                        <input type="number" class="form-control" min="0" max="10000000" step="1" ng-model="addedVolume">
                    </div>
                </div>
                <div class="form-group">
                    <label class="col-sm-3 control-label">{4}</label>
                    <div class="col-sm-2">
                        <input type="number" class="form-control" min="0.001" max="100" step="0.001" ng-model="addedGravity">
                    </div>
                    <p class="help-block col-sm-3">{5}</p>
                </div>
                <div class="form-group">
                    <label class="col-sm-3 control-label">{6}</label>
                    <div class="col-sm-2">
                        <input type="number" class="form-control" min="0" max="10000000" step="1" ng-change="finalVolChanged()" ng-model="finalVol">
                    </div>
                </div>
                <div class="form-group tool-result">
                    <label class="col-sm-3 control-label">{7}</label>
                    <div class="col-sm-2">
                        <label class="control-label">{8}</label>
                    </div>
                </div>
                </form>
            </div>
        </div>'''.format(QCoreApplication.translate("Export","Dilution", None, QCoreApplication.UnicodeUTF8),QCoreApplication.translate("Export","Volume initial (L)", None, QCoreApplication.UnicodeUTF8),QCoreApplication.translate("Export","Densité spécifique initiale", None, QCoreApplication.UnicodeUTF8),QCoreApplication.translate("Export","Volume ajouté (L)", None, QCoreApplication.UnicodeUTF8),QCoreApplication.translate("Export","Densité de l'ajout", None, QCoreApplication.UnicodeUTF8),QCoreApplication.translate("Export","1 si ajout d'eau", None, QCoreApplication.UnicodeUTF8),QCoreApplication.translate("Export","Volume final (L)", None, QCoreApplication.UnicodeUTF8),QCoreApplication.translate("Export","Densité spécifique finale", None, QCoreApplication.UnicodeUTF8),"{{calcDilution()}}")
        
        
    resultHtml+='''<div class="row row-tools" id="boiloff">
            <div ng-controller="BoiloffToolCtrl" class="tool-block">
                <h3>{0}</h3>
                <form class="form-horizontal" role="form">
                <div class="form-group">
                    <label class="col-sm-3 control-label">{1}</label>
                    <div class="col-sm-2">
                        <input type="number" class="form-control" min="0" max="10000000" step="1" ng-model="preboilVol">
                    </div>
                </div>
                <div class="form-group">
                    <label class="col-sm-3 control-label" >{2}</label>
                    <div class="col-sm-2">
                        <input type="number"  class="form-control" min="0.001" max="100" step="0.001" ng-model="preboilGravity">
                    </div>
                </div>
                <div class="form-group">
                    <label class="col-sm-3 control-label">{3}</label>
                    <div class="col-sm-2">
                        <input type="number" class="form-control" min="0" max="10000000" step="1" ng-model="boilOffRate">
                    </div>
                </div>
                <div class="form-group">
                    <label class="col-sm-3 control-label">{4}</label>
                    <div class="col-sm-2">
                        <input type="number" class="form-control" min="1" max="100000" step="10" ng-model="boilTime">
                    </div>
                    
                </div>
                <div class="form-group">
                    <label class="col-sm-3 control-label">{5}</label>
                    <div class="col-sm-2">
                        <input type="number" class="form-control" min="0" max="10000000" step="1" ng-change="" ng-model="coolingLoss">
                    </div>
                </div>
                <div class="form-group tool-result">
                    <label class="col-sm-3 control-label">{6}</label>
                    <div class="col-sm-2">
                        <label class="control-label">{7}</label>
                    </div>
                </div>
                <div class="form-group ">
                    <label class="col-sm-3 control-label">{8}</label>
                    <div class="col-sm-2">
                        <label class="control-label">{9}</label>
                    </div>
                </div>
                <div class="form-group ">
                    <label class="col-sm-3 control-label">{10}</label>
                    <div class="col-sm-2">
                        <label class="control-label">{11}</label>
                    </div>
                </div>
                <div class="form-group ">
                    <label class="col-sm-3 control-label">{12}</label>
                    <div class="col-sm-2">
                        <label class="control-label">{13}</label>
                    </div>
                </div>
                </form>
            </div>
        </div>''' .format(QCoreApplication.translate("Export","Evaporation", None, QCoreApplication.UnicodeUTF8),
            QCoreApplication.translate("Export","Volume pré-ébullition (L)", None, QCoreApplication.UnicodeUTF8),
            QCoreApplication.translate("Export","Densité spécifique pré-ébullition", None, QCoreApplication.UnicodeUTF8),
            QCoreApplication.translate("Export","Taux d'évaporation (%/heure)", None, QCoreApplication.UnicodeUTF8),
            QCoreApplication.translate("Export","Durée d'ébullition (min)", None, QCoreApplication.UnicodeUTF8),
            QCoreApplication.translate("Export","Pertes par refroidissement (%)", None, QCoreApplication.UnicodeUTF8),
            QCoreApplication.translate("Export","Volume évaporé (ébullition) (L)", None, QCoreApplication.UnicodeUTF8),
            "{{calcBoilOff().boilOffVol}}",            
            QCoreApplication.translate("Export","Volume évaporé (refroidissement) (L)", None, QCoreApplication.UnicodeUTF8),
            "{{calcBoilOff().coolingLoss}}",
            QCoreApplication.translate("Export","Volume final (L)", None, QCoreApplication.UnicodeUTF8),
            "{{calcBoilOff().finalVol}}",
            QCoreApplication.translate("Export","Densité spécifique", None, QCoreApplication.UnicodeUTF8),
            "{{calcBoilOff().finalSg}}")
        
        
    resultHtml+='''<div class="row row-tools" id="decoc">
            <div ng-controller="DecocToolCtrl" class="tool-block">
                <h3>{0}</h3>
                <form class="form-horizontal" role="form">
                <div class="form-group">
                    <label class="col-sm-3 control-label">{1}</label>
                    <div class="col-sm-2">
                        <input type="number" class="form-control" min="0" max="100000" step="1" ng-model="mashVol">
                    </div>
                </div>
                <div class="form-group">
                    <label class="col-sm-3 control-label">{2}</label>
                    <div class="col-sm-2">
                        <input type="number" class="form-control" min="0" max="100" step="1" ng-model="targetTemp">
                    </div>
                </div>
                <div class="form-group">
                    <label class="col-sm-3 control-label">{3}</label>
                    <div class="col-sm-2">
                        <input type="number" class="form-control" min="0" max="100000" step="1" ng-model="startTemp">
                    </div>
                </div>
                <div class="form-group">
                    <label class="col-sm-3 control-label">{4}</label>
                    <div class="col-sm-2">
                        <input type="number" class="form-control" min="0" max="1000" step="1" ng-model="boilTemp">
                    </div>
                </div>
                <div class="form-group">
                    <label class="col-sm-3 control-label">{5}</label>
                    <div class="col-sm-2">
                        <input type="number" class="form-control" min="0" max="1000" step="1" ng-model="correction">
                    </div>
                </div>
                <div class="form-group tool-result">
                    <label class="col-sm-3 control-label">{6}</label>
                    <div class="col-sm-2">
                        <label class="control-label">{7}</label>
                    </div>
                </div>
                <div class="form-group">
                    <label class="col-sm-3 control-label">{8}</label>
                    <div class="col-sm-2">
                        <label class="control-label">{9}</label>
                    </div>
                </div>
                </form>
            </div>
        </div>'''.format(QCoreApplication.translate("Export","Décoction", None, QCoreApplication.UnicodeUTF8),
            QCoreApplication.translate("Export","Volume de moût (L)", None, QCoreApplication.UnicodeUTF8),
            QCoreApplication.translate("Export","Température cible (°C)", None, QCoreApplication.UnicodeUTF8),
            QCoreApplication.translate("Export","Température de départ (°C)", None, QCoreApplication.UnicodeUTF8),
            QCoreApplication.translate("Export","Température d'ébullition (°C)", None, QCoreApplication.UnicodeUTF8),
            QCoreApplication.translate("Export","Facteur de correction (%)", None, QCoreApplication.UnicodeUTF8),
            QCoreApplication.translate("Export","Volume de décoction (L)", None, QCoreApplication.UnicodeUTF8),
            "{{calcDecoction().decocVol}}",
            QCoreApplication.translate("Export","Fraction du moût (%)", None, QCoreApplication.UnicodeUTF8),
            "{{calcDecoction().fraction}}"
            )
        
        
    resultHtml+='''<div class="row row-tools last" id="sg">
            <div ng-controller="SgPlatoToolCtrl" class="tool-block">
                <h3>{0}</h3>
                <form class="form-horizontal" role="form">
                <div class="form-group">
                    <label class="col-sm-3 control-label">{1}</label>
                    <div class="col-sm-2">
                        <input type="number" class="form-control" min="0" max="10" step="0.001" ng-model="specificGravity" ng-change="sgChanged()">
                    </div>
                </div>
                <div class="form-group">
                    <label class="col-sm-3 control-label">{2}</label>
                    <div class="col-sm-2">
                        <input type="number" class="form-control" min="0" max="100" step="1" ng-model="plato" ng-change="platoChanged()">
                    </div>
                </div>
                </div>
                </form>
            </div>
        </div>

    <!-- Fin container -->
    </div>

<script type="text/javascript">
                    $(function () {
                    $("[data-toggle='dropdown']").dropdown();
                    });
</script>    
</body>
</html>''' .format(QCoreApplication.translate("Export","Densité spécifique - Plato", None, QCoreApplication.UnicodeUTF8),
            QCoreApplication.translate("Export","Densité spécifique", None, QCoreApplication.UnicodeUTF8),
            QCoreApplication.translate("Export","Plato", None, QCoreApplication.UnicodeUTF8))

    

    return resultHtml


