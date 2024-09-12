from enums import TruthOrDareQuestionType
from models import Prediction, TruthOrDareQuestion, Wish
from repositories import APIRepository, handle_server_api_errors

__all__ = ('QuizRepository',)


class QuizRepository(APIRepository):

    async def get_random_wish(self) -> Wish:
        response = await self._http_client.get('/quizzes/wishes/random/')

        response_data = response.json()

        if response.is_error:
            handle_server_api_errors(response_data['errors'])

        return Wish.model_validate(response_data)

    async def get_random_prediction(self) -> Prediction:
        response = await self._http_client.get('/quizzes/predictions/random/')

        response_data = response.json()

        if response.is_error:
            handle_server_api_errors(response_data['errors'])

        return Prediction.model_validate(response_data)

    async def get_random_truth_or_dare_question(
            self,
            *,
            question_type: TruthOrDareQuestionType | None = None,
    ) -> TruthOrDareQuestion:
        url = '/quizzes/truth-or-dare/random/'
        query_params = {}
        if question_type is not None:
            query_params['type'] = question_type

        response = await self._http_client.get(url, params=query_params)

        response_data = response.json()

        if response.is_error:
            handle_server_api_errors(response_data['errors'])

        return TruthOrDareQuestion.model_validate(response_data)
