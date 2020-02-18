import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pyApi.settings")
import django
django.setup()
from wearers.models import Licence
#from snippets.serializers import SnippetSerializer
#from django.contrib.auth.models import User


def populateLicence():
    l = Licence(versionStr = 'None',
                summary = "Not Agreed to a Licence",
                text = "Not Agreed to a Licence - can not use this data")
    l.save()
    l = Licence(versionStr = '1.0',
                summary = "Anonymised Data can be Published",
                text = "The OpenSeizureDetector team has access to your personal data such as email address.  We will only use this to contact you in the event of a query about the data.   The team has access to the data recorded by the watch and any categories annotations you have provided, such as categorising events.   We will use this data to develop improved seizure detection algorithms that will be made available in future releases of OpenSeizureDetector."
" The data recorded by the watch will be published in an anonymised form to allow others to compare seizure detection algorithms with a view to improving knowledge of seizures and their detection.   No personal data will be provided with the published data.")
    l.save()
