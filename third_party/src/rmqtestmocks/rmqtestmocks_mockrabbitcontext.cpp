// Copyright 2020-2023 Bloomberg Finance L.P.
// SPDX-License-Identifier: Apache-2.0
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#include <rmqtestmocks_mockrabbitcontext.h>

namespace BloombergLP {
namespace rmqtestmocks {
MockRabbitContext::MockRabbitContext() {}
MockRabbitContext::~MockRabbitContext() {}

bsl::shared_ptr<rmqa::RabbitContext> MockRabbitContext::context()
{
    bslma::ManagedPtr<rmqp::RabbitContext> context(
        this, bslma::Default::allocator(), bslma::ManagedPtrUtil::noOpDeleter);

    return bsl::shared_ptr<rmqa::RabbitContext>(
        new rmqa::RabbitContext(context));
}

} // namespace rmqtestmocks
} // namespace BloombergLP
