// import store from '@/store';
// import log from './logger';

export default async (router = '', data = {}, method = 'GET', type = 'json') => {
  console.log(new Date());
  console.log('data:', data);
  const reqMethod = method.toUpperCase();
  const reqUrl = router;
  const requestConfig = {
    method: reqMethod,
    // headers: {
    //   Authorization: 'Bearer '.concat(store.getters.token),
    // },
    // headers: {
    //   'Access-Control-Allow-Origin': 'http://localhost:8080',
    // },
  };
  if (type === 'json') {
    requestConfig['Content-Type'] = 'application/json';

    if (method === 'POST') {
      requestConfig.body = JSON.stringify(data);
    }
  }

  if (type === 'form-data') {
    const formData = new FormData();
    Object.keys(data).forEach((key) => {
      formData.append(key, data[key]);
    });
    requestConfig.body = formData;
  }
  console.log('requestConfig:', requestConfig);

  try {
    console.log('before fetch');
    response = await fetch(reqUrl, requestConfig);
    console.log('response:', response);
  } catch (error) {
    /* if response body is null, it will catch error */
    /* eslint no-empty: "error" */
    response = error;
    console.log('response:', response);
  }
  return new Promise((resolve, reject) => {
    console.log('response:', response);
    if (!response.ok) {
        reject(response.json())
    } else{
        resolve(response.json())
    }
  });
};
