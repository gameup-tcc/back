from games.models import Game, Report, Evaluation
from games.serializers import GameSerializer, ReportSerializer, EvaluationSerializer
from rest_framework import generics
from django.http import Http404, HttpResponse, JsonResponse
from django.views.generic.base import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from attributes import ATTRIBUTES_WEIGHTS
from assessment import ASSESSMENT_WEIGHTS

class GameList(generics.ListCreateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

class GameDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

class EvaluationList(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication, JSONWebTokenAuthentication)
    permission_classes = (IsAuthenticated,)
    def get(self, request, fk, format=None):
        reports = Evaluation.objects.filter(game=fk)
        serializer = EvaluationSerializer(reports, many=True)
        return Response(serializer.data)

    def post(self, request, fk, format=None):
        serializer = EvaluationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EvaluationDetail(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication, JSONWebTokenAuthentication)
    permission_classes = (IsAuthenticated,)
    def get_object(self, pk, fk):
        try:
            return Evaluation.objects.get(game=fk, pk=pk)
        except Evaluation.DoesNotExist:
            raise Http404

    def get(self, request, pk, fk, format=None):
        evaluation = self.get_object(pk, fk)
        serializer = EvaluationSerializer(evaluation)
        return Response(serializer.data)

    def put(self, request, pk, fk, format=None):
        serializer = EvaluationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, fk, format=None):
        evaluation = self.get_object(pk, fk)
        evaluation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BloomReport(View):
    def get(self, request, fk):
        report = self.reportAnalysis(fk)
        return JsonResponse(report)

    ###

    def getAllEvaluations(self, fk):
        return Evaluation.objects.filter(game_id=fk, eval_type='BL')

    def reportAnalysis(self, fk):
        subProcessCount = {}
        evaluations = self.getAllEvaluations(fk)

        for evaluation in evaluations:
            subProcessCount = self.countSubProcesses(evaluation.result, subProcessCount)

        processTotal = self.summarizeProcesses(subProcessCount)
        assessmentTotal = self.summarizeAssessment(subProcessCount)
        topSubProcesses= self.summarizeTopSubProcesses(subProcessCount)

        report = {'process': processTotal, 'topSubProcesses': topSubProcesses, 'assessment': assessmentTotal}
        return report

    def countSubProcesses(self, submission, subProcessCount):
        for process, subProcess in submission.iteritems():
            if process not in subProcessCount:
                subProcessCount[process] = {}

            for sub in subProcess:
                if sub not in subProcessCount[process]:
                    subProcessCount[process][sub] = 0

                if subProcess[sub]:
                    subProcessCount[process][sub] += 1

        return subProcessCount

    def summarizeProcesses(self, subProcessCount):
        processTotal = [0 for i in range(7)]

        for process, subProcesses in subProcessCount.iteritems():
            for sub in subProcesses:
                processTotal[int(process)] += subProcesses[sub]

        return processTotal

    def summarizeAssessment(self, subProcessCount):
        assessmentTotal = [0 for i in range(18)]

        for process, subProcesses in subProcessCount.iteritems():
            for sub in subProcesses:
                for i in range(6):
                    subProcessNumber = int(sub[1:]) - 1
                    assessmentTotal[i+1] += (subProcesses[sub]*ASSESSMENT_WEIGHTS[subProcessNumber][i])

        return assessmentTotal

    def summarizeTopSubProcesses(self, subProcessCount):
        sorted_subProcess = map(lambda x: x[1].items(), subProcessCount.iteritems())
        sorted_subProcess = [y for x in sorted_subProcess for y in x]
        sorted_subProcess = sorted(sorted_subProcess, key=lambda x: x[1], reverse=True)
        return sorted_subProcess


class GamificationReport(View):
    def get(self, request, fk):
        report = self.reportAnalysis(fk)
        return JsonResponse(report)

    ###

    def getAllEvaluations(self, fk):
        return Evaluation.objects.filter(game_id=fk, eval_type='GA')

    def reportAnalysis(self, fk):
        tecCount = {}
        evaluations = self.getAllEvaluations(fk)

        for evaluation in evaluations:
            tecCount = self.countTechniques(evaluation.result, tecCount)

        coreTotal = self.summarizeCoreDrives(tecCount)
        attrTotal = self.summarizeAttributes(tecCount, len(evaluations))
        topTechniques = self.summarizeTopTechniques(tecCount)

        report = {'coreDrive': coreTotal, 'attributes': attrTotal, 'topTechniques': topTechniques}
        return report

    def countTechniques(self, submission, tecCount):
        for coreDrive, techniques in submission.iteritems():
            if coreDrive not in tecCount:
                tecCount[coreDrive] = {}

            for technique in techniques:
                if technique not in tecCount[coreDrive]:
                    tecCount[coreDrive][technique] = 0

                if techniques[technique]:
                    tecCount[coreDrive][technique] += 1

        return tecCount

    def summarizeCoreDrives(self, tecCount):
        coreTotal = [0 for i in range(9)]

        for coreDrive, techniques in tecCount.iteritems():
            for technique in techniques:
                coreTotal[int(coreDrive)] += techniques[technique]

        return coreTotal

    def summarizeAttributes(self, tecCount, totalCount):
        attrTotal = [0 for i in range(7)]

        for coreDrive, techniques in tecCount.iteritems():
            for technique in techniques:
                for i in range(6):
                    techniqueNumber = int(technique[1:]) - 1
                    attrTotal[i+1] += (techniques[technique]*ATTRIBUTES_WEIGHTS[techniqueNumber][i])

        return attrTotal

    def summarizeTopTechniques(self, tecCount):
        ordered_tech = map(lambda x: x[1].items(), tecCount.iteritems())
        ordered_tech = [y for x in ordered_tech for y in x]
        ordered_tech = sorted(ordered_tech, key=lambda x: x[1], reverse=True)
        return ordered_tech


