import re
from abc import ABC, abstractmethod
import math

from service.enums import Algorithm
from service.entities import (
    CheckInput,
    CheckResult
)
from Levenshtein import jaro, jaro_winkler, hamming, distance


class AntiplagBaseService(ABC):

    @abstractmethod
    def check_plagiarism(self, data: CheckInput) -> str:
        pass
    
    def _normalize(self, text: str) -> str:
        new_words = []
        for word in text:
            w = re.sub(r'[^\w\s]','',word)
            w = re.sub(r'_','',w)
            new_words.append(w)
        return "".join(new_words)
    


class LevenshteinService(AntiplagBaseService):

    def check_plagiarism(self, data: CheckInput):

        name: str = data['name']
        ref_text: str = data['ref_text']
        candidate_text: str = data['candidate_text']

        norm_ref = self._normalize(ref_text)
        norm_cand = self._normalize(candidate_text)


        match name:
            case 'Расстояние Левенштейна':                
                result = (1 - (distance(norm_ref, norm_cand)/max(len(norm_ref), len(norm_cand))))
            case 'Расстояние Джаро-Винклера':
                result = jaro_winkler(norm_ref, norm_cand)
            case 'Расстояние Джаро':
                result = jaro(norm_ref, norm_cand)
            case 'Расстояние Хэмминга':
                if (len(norm_cand)!=len(norm_ref)):
                    result = "Ошибка! Длины строк не совпадают."
                else:
                    result = 1 - (hamming(norm_ref, norm_cand) / len(norm_cand))

        if type(result) != str:
            percent = f'{round(result, 2) * 100}%'
        else:
            percent = result
        return CheckResult(percent=percent)


class ShingleService(AntiplagBaseService):

    def check_plagiarism(self, data: CheckInput):
        name: str = data['name']
        ref_text: str = data['ref_text']
        candidate_text: str = data['candidate_text']

        norm_ref = self._normalize(ref_text)
        norm_cand = self._normalize(candidate_text)
        
        k = 3
        # Разбиваем первую строку на список shingle-блоков
        shingles1 = set()
        for i in range(len(norm_ref) - k + 1):
            shingles1.add(norm_ref[i:i+k])

        # Разбиваем вторую строку на список shingle-блоков
        shingles2 = set()
        for i in range(len(norm_cand) - k + 1):
            shingles2.add(norm_cand[i:i+k])

        # Вычисляем сходство
        result = float(len(shingles1.intersection(shingles2))) / float(len(shingles1.union(shingles2)))

        percent = f'{math.trunc(round(result, 2) * 100)}%'
        return CheckResult(percent=percent)
    



class AntiplagService:

    def check(self, data: CheckInput):

        """ Проверка текста на наличие в нем плагиата. """

        name: str = data['name']

        if name in Algorithm.LEV_ALGS:
            service = LevenshteinService()
        elif name == Algorithm.SH:
            service = ShingleService()
        return service.check_plagiarism(data)
