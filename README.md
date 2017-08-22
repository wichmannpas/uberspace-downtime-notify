uberspace-downtime-notify
=========================

A simple script which checks the twitter account of uberspace (or any other twitter account as well) for messages containing specific keywords.

To use this script, adopt the RELEVANT_HOSTS variable to fit your needs. If you can not delay emails locally (or want to deliver them to another user), change the NOTIFY_COMMAND, too.

A possible deployment would be in a cronjob on an uberspace account which launches the script once (or maybe twice) per day.

Example Deployment on a Uberspace Host
--------------------------------------

Clone this repository on the remote host, for example:

    git clone https://github.com/wichmannpas/uberspace-downtime-notify.git
    cd uberspace-downtime-notify

Specify the hosts relevant to you in the RELEVANT_HOSTS variable in the file `fetch.py`.

Configure a cronjob (i.e., `crontab -e`), for example this line to check all six hours:

    0  */6    *   *   *   python $HOME/uberspace-downtime-notify/fetch.py

Notification emails quoting the relevant Twitter thread will be sent to your primary email address of your Uberspace account (you can change this behaviour in the NOTIFY_COMMAND variable).

A hash of each sent message is stored in a file to notify you only once.


License
-------

Copyright 2016 Pascal Wichmann

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
